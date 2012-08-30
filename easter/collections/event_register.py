# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from easter.mixins.mongoable import Mongoable
from easter.utils.exceptions import NotExistsException

class RegisteredEvents(Mongoable):
  '''
    注册的事件表。app_name和collection_name作为唯一字段。
    可以指定的字段：
    1. event_app app的名字
    2. event_collection collection的名字
    3. time_stat 记录时间的字段。可以申明为组合。比如clip__board
    4. total_stat 需要统计的字段，可以给条件选取。比如{origin: {1: web, 2: app}} 当origin为1时是web
    5. event_unique 唯一字段表
    6. event_fields_to_db 需要记录到event表中的字段，默认记录unique，date
    7. event_fields_to_feeds 需要push到user_events中的字段。默认推送时间和名字
    8. event_indexes. 指定的indexes，默认将unique作为indexes
    9. event_alias 记录的表明，比如{'clip': 'c'} 所有的clip相关的名字用c来指代。
  '''
  app_name = 'easter'
  collection_name = 'register_events'

  unique_fields = ['event_app', 'event_collection']
  indexes = [(dict.fromkeys(unique_fields, 1), {'unique': True}), ]

  def __init__(self, event_app, event_name, time_stat=[],
               total_stat=[], event_unique=[], event_fields_to_db=[],
               event_fields_to_feeds=[], event_indexes=[], event_alias={}):
    self.event_app = event_app
    self.event_name = event_name
    self.time_stat = time_stat
    self.total_stat = total_stat
    self.event_unique = event_unique
    self.event_fields_to_db = event_fields_to_db
    self.event_fields_to_feeds = event_fields_to_feeds
    self.event_indexes = event_indexes
    self.event_alias = event_alias

  @classmethod
  def get_by_name(cls, event_app, event_name):
    json_data = cls.get_one_query({'event_app': event_app, 'event_name': event_name})
    if not json_data:
      raise NotExistsException("Not exists app_name %s, collection_name %s" %(event_app, event_collection))

    data = cls.format_data(json_data)
    return data


  @classmethod
  def format_data(cls, json_data):
    app_name = json_data['event_app']
    collection_name = json_data['event_name']
    record_time_fields = json_data.get('time_stat', [])
    record_total_fields = json_data.get('total_stat', [])
    unique_fields = json_data.get('event_unique', [])
    fields_to_db = json_data.get('event_fields_to_db', [])
    event_pull_fields = json_data.get('event_fields_to_feeds', [])
    indexes = json_data.get('event_indexes', [])
    alias = json_data.get('event_alias', {})

    return {
      'app_name': app_name,
      'collection_name': collection_name,
      'record_time_fields': record_time_fields,
      'record_total_fields': record_total_fields,
      'unique_fields': unique_fields,
      'fields_to_db': fields_to_db,
      'event_pull_fields': event_pull_fields,
      'indexes': indexes,
      'alias': alias
    }