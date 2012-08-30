# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from easter.core.mongo import get_mongodb
from easter.utils.exceptions import NotExistsException, MongoDBHandleException

import logging

logger = logging.getLogger()

class Mongoable:
  """
  自己抽象的mongo ORM Mixin。需要ORM的model可以继承这个类。
  TODO：BUG 多多。需要修复！！
  1. 不应该用dict信息。里面有很多不相关的东西。vars(obj)??? 用户自定义???
  2. 封装得不智能。耦合度太高。主要在query上面
  3. 如何更人性化的处理id问题。
  """

  @property
  def unique(self):
    raise NotImplemented

  @classmethod
  def cls_unique(cls, **kwargs):
    raise NotImplemented

  @classmethod
  def get_collection(cls):
    db = get_mongodb(cls.app_name)
    return db[cls.collection_name]

  def dict_to_db(self):
    return self.__dict__

  def save(self):
    collection = self.get_collection()
    try:
      collection.insert(self.dict_to_db())
    except Exception, err:
      logger.info(err)
      raise MongoDBHandleException('On Save')
    else:
      return True

  def exists(self):
    try:
      instance = self.get_one_query(query=self.unique)
    except Exception, err:
      logger.info(err)
      return False
    
    return bool(instance)

  def update(self, obj, upsert=True):
    collection = self.get_collection()

    try:
      collection.update(self.unique, obj, upsert=upsert)
    except Exception, err:
      logger.info(err)
      raise MongoDBHandleException('On Instance Update')

  @classmethod
  def cls_update(cls, obj, upsert=True, **kwargs):
    collection = cls.get_collection()

    try:
      collection.update(cls.cls_unique(**kwargs), obj, upsert=upsert)
    except Exception, err:
      logger.info(err)
      raise MongoDBHandleException('On Class Update')

  @classmethod
  def objects(cls):
    collection = cls.get_collection()
    all = collection.find()

    if not all:
      raise StopIteration

    for item in all:
      del item['_id']
      yield cls(**item)

  @classmethod
  def get_one_query(cls, query, only=[]):
    restrict = dict.fromkeys(only, 1)
    collection = cls.get_collection()

    try:
      if not restrict:
        json_data = collection.find_one(query)
      else:
        json_data = collection.find_one(query, restrict)
    except Exception, err:
      logger.info(err)
      raise MongoDBHandleException("On Cls Get One Query")

    else:
      if not json_data:
        raise NotExistsException("Not Exists mongodb query %s" %query)
  
      if json_data.has_key('_id'):
        del json_data['_id']
      return json_data

  @classmethod
  def get_by_query(cls, query, only=[]):
    restrict = dict.fromkeys(only, 1)
    collection = cls.get_collection()

    try:
      if not restrict:
        clusters = collection.find(query)
      else:
        restrict.update(dict.fromkeys(cls.unique_fields, 1))
        clusters = collection.find(query, restrict)
    except Exception, err:
      logger.info(err)
      raise MongoDBHandleException("On Cls Get by Query")

    else:
      clusters = list(clusters)
      for cluster in clusters:
        if cluster.has_key('_id'):
          del cluster['_id']
      return clusters

  @classmethod
  def get_indexes(cls):
    collection = cls.get_collection()
    return collection.index_information()

  @classmethod
  def ensure_indexes(cls):
    if not getattr(cls, 'indexes', None):
      return

    assert isinstance(cls.indexes, list)
    collection = cls.get_collection()

    try:
      for index, extra in cls.indexes:
        key_list = index.items()
        collection.ensure_index(key_list, **extra)

    except Exception, err:
      logger.info(err)
      raise MongoDBHandleException("On Ensure indexes")

  @classmethod
  def clear_indexes(cls):
    collection = cls.get_collection()

    try:
      collection.drop_indexes()
    except Exception, err:
      logger.info(err)
      raise MongoDBHandleException("On Clear indexes")

  @classmethod
  def delete_all(cls):
    collection = cls.get_collection()
    collection.remove()

  @classmethod
  def delete(cls, query):
    collection = cls.get_collection()
    collection.remove(query)