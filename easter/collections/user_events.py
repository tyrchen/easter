# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

import logging
from easter.mixins.recordable import BaseRecord
from datetime import datetime as py_time
from easter.utils.util import to_datetime as str_to_datetime

logger = logging.getLogger(__name__)

class UserEventFalls(BaseRecord):
  """
    记录用户时间，以时间为维度。更具uid和时间取出相应的数据.
  """
  app_name = 'cayman'
  collection_name = 'user_events'

  unique_fields = ['uid', 'datetime']
  indexes = [({'uid': 1}, {}),
    (dict.fromkeys(unique_fields, 1), {'unique': True}),]

  def __init__(self, uid, datetime=py_time.now(), **kwargs):
    self.uid = uid
    if isinstance(datetime, basestring):
      datetime = py_time.strptime(datetime, '%Y-%m-%d %H:%M:%S')

    self.datetime = datetime
    self.__dict__.update(kwargs)

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

  @classmethod
  def merge(cls, from_uid, to_uid):
    collection = cls.get_collection()
    try:
      collection.update({'uid': from_uid},
          {'$set': {'uid': to_uid, 'cookie': from_uid}}, upsert=False, multi=True)
    except Exception, err:
      logger.info(err)

  @classmethod
  def get(cls, uid=None, from_datetime=py_time.now(), to_datetime=py_time.now(), only=[]):
    if isinstance(from_datetime, basestring):
      from_datetime = str_to_datetime(from_datetime)
    if isinstance(to_datetime, basestring):
      to_datetime = str_to_datetime(to_datetime)

    if uid:
      cursors = cls.get_by_query({'uid': uid, 'datetime':{
          '$gte': from_datetime, '$lt': to_datetime}}, only=only)
    else:
      cursors  = cls.get_by_query({'datetime': {
          '$gte': from_datetime, '$lt': to_datetime}}, only=only)
    return cursors