# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from easter.collections.user_events import UserEventFalls
from easter.core.interpreter import StatTemplateInterpreter
from easter.mixins.recordable import BaseRecord
from easter.mixins.time_stat import TimeStatistics
from easter.mixins.total_stat import TotalStatistics
from datetime import datetime as py_time, timedelta
from easter.utils.helper import merge_dicts
from easter.utils.util import using_hours, document_datetime
from easter.utils.util import to_datetime as str_to_datetime
from django.conf import settings

import logging

logger = logging.getLogger(__name__)
ONE_HOUR = settings.ONE_HOUR or 3600
ONE_DAY = settings.ONE_DAY or 3600*24

class EventFactory(object):
  @classmethod
  def produce(cls, cls_info):
    e = EventHandler
    e.__dict__.update(cls_info)
    return e

class EventHandler(BaseRecord, TimeStatistics, TotalStatistics):
  '''
    module中最关键的一个collection.加入了BaseRecord, TimeStat, TotalStat Mixin。
    有两个主要作用：
    1. 基于总计统计某些行为。
    2. 基于时间轴(以小时为基数)来统计行为。
    我们采用注册的机制，只有注册的行为才能统计。不然请求会被返回。
  '''
  app_name = ''
  collection_name = ''

  record_time_fields = []
  record_total_fields = []
  unique_fields = ['date']
  fields_to_db = []
  event_pull_fields = []
  indexes = [(dict.fromkeys(unique_fields, 1), {'unique': True}), ]
  alias = {}

  def __init__(self, uid, **kwargs):
    self.uid = uid
    datetime = kwargs.pop('datetime', '')
    if not datetime:
      datetime = py_time.now()
    else:
      datetime = py_time.strptime(datetime, '%Y-%m-%d %H:%M:%S')

    self.datetime = datetime
    date = self.datetime.date()
    self.date = py_time(year=date.year, month=date.month, day=date.day)
    kwargs.pop('uid', '')
    kwargs.pop('date', '')
    self.__dict__.update(kwargs)
    self.init_hook()

  def init_hook(self):
    """
      实例化一些额外的字段。比如事件的总体统计信息等。
      现在默认统计两个字段，事件的总计和事件的触发时间统计。
    """
    if 'event_total' not in self.record_total_fields:
      self.record_total_fields.append('event_total')
    if 'total' not in self.time_record_fields():
      self.record_time_fields.append('total')
    if not hasattr(self, 'origin'):
      self.origin = '0'

  def dict_to_db(self):
    record_dict = {}
    for field in self.fields_to_db:
      record_dict.update({field: getattr(self, field, '')})
    record_dict.update({'date': self.date})
    return record_dict

  @property
  def unique(self):
    unique_dict = {}
    for field in self.unique_fields:
      value = getattr(self, field)
      unique_dict.update({field: value})
    return unique_dict

  @classmethod
  def cls_unique(cls, **kwargs):
    unique_dict = {}
    for field in cls.unique_fields:
      value = kwargs.pop(field, '')
      unique_dict.update({field: value})
    return unique_dict

  def time_record_fields(self):
    return StatTemplateInterpreter.parse(self, self.record_time_fields, alias=self.alias)

  def total_record_fields(self):
    return StatTemplateInterpreter.parse(self, self.record_total_fields, alias=self.alias)

  def pushable_fields(self):
    return self.event_pull_fields

  def update_objs(self):
    update_time_objs = self.time_record(self.datetime)
    update_total_objs = self.total_record()
    merged_dict = merge_dicts(update_time_objs, update_total_objs)
    return merged_dict

  def after_update(self):
    if not (self.event_pull_fields and hasattr(self, 'uid')):
      return

    pull_data = {}
    for field in self.event_pull_fields:
      value = getattr(self, field, '')
      pull_data.update({field: value})

    pull_data.update({'datetime': self.datetime,
                      'event_name': self.collection_name
                    })
    u = UserEventFalls(uid=self.uid, **pull_data)
    u.record()

  @classmethod
  def get(cls, date, fields=[]):
    return cls.get_by_query(query={'date': date}, only=fields)

  @classmethod
  def mget(cls, from_datetime=py_time.now(), to_datetime=py_time.now(), fields=[]):
    if isinstance(from_datetime, basestring):
      from_datetime = str_to_datetime(from_datetime)
    if isinstance(to_datetime, basestring):
      to_datetime = str_to_datetime(to_datetime)

    hour_handler = using_hours(from_datetime=from_datetime, to_datetime=to_datetime)
    if hour_handler:
      return cls.mget_hours(from_datetime, to_datetime, fields)
    else:
      return cls.mget_days(from_datetime, to_datetime, fields)

  @classmethod
  def mget_hours(cls, from_datetime=py_time.now(), to_datetime=py_time.now(), fields=[]):
    delta = timedelta(hours=24)
    from_yesterday = from_datetime - delta
    to_tomorrow = to_datetime + delta
    cursors = cls.get_by_query(query={'date': {'$gte': from_yesterday, '$lt': to_tomorrow}}, only=fields)
    infos = []

    #WARING TODO: 可能出现跨小时问题。
    def total_hours(from_datetime, to_datetime): #统计总共需要返回多少个小时
      delta = to_datetime - from_datetime
      return int(delta.total_seconds() / ONE_HOUR)

    for field in fields: #初始化数组，给默认值
      info = {}
      info['total'] = 0
      info["stats"] = [0 for i in range(total_hours(from_datetime, to_datetime))]
      infos.append(info)

    # Fucking!!!Dirty code.
    for cursor in cursors:
      date = cursor['date']
      for i, field in enumerate(fields): #迭代每个field
        data = cursor.get(field, 0)
        if isinstance(data, dict): #如果是dict，表明统计的是时间
          for hour in data:
            d_time = document_datetime(date, hour) #lazy的做法，将小时加上document的date，和请求时间比较
            if not (d_time >= from_datetime and d_time <= to_datetime):
              continue
            infos[i]["total"] += data[hour]
            which_hour = total_hours(from_datetime, d_time) #在返回值的具体位置上设置
            infos[i]["stats"][which_hour] = data[hour]
        else:
          infos[i]["total"] += data
          infos[i]["stats"] = data
    return infos


  @classmethod
  def mget_days(cls, from_datetime=py_time.now(), to_datetime=py_time.now(), fields=[]):
    delta = timedelta(hours=24)
    from_yesterday = from_datetime - delta
    to_tomorrow = to_datetime + delta
    cursors = cls.get_by_query(query={'date': {'$gte': from_yesterday, '$lt': to_tomorrow}}, only=fields)
    def total_days(from_datetime, to_datetime):
      delta = to_datetime - from_datetime
      days = int(delta.total_seconds() / ONE_DAY) if not delta.total_seconds() < 0 else -1
      return days + 1

    infos = []
    for field in fields:
      info = {}
      info["total"] = 0
      info["stats"] = [0 for i in range(total_days(from_datetime, to_datetime))]
      infos.append(info)

    for cursor in cursors:
      date = cursor['date']
      for i, field in enumerate(fields):
        data = cursor.get(field, 0)
        total = 0
        if isinstance(data, dict):
          for hour in data:
            d_time = document_datetime(date, hour)
            if not (d_time >= from_datetime and d_time <= to_datetime):
              continue
            total += data[hour]
        else:
          total = data
        which_day = total_days(from_datetime, date)
        infos[i]['total'] += total
        infos[i]['stats'][which_day] = total
    return infos
