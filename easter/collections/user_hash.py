# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from easter.mixins.mongoable import Mongoable

import logging
logger = logging.getLogger(__name__)

class UserHashTable(Mongoable):
  """
  定义了用户hashtable。主要记录用户的cookie和id对应的关系。
  目的是链接用户登录前后关系。
  """
  app_name = 'easter'
  collection_name = 'user_hash'
  indexes = [({'user_hash': 1}, {'unique': True})]

  class MD5Hash:
    def hexdigest(self, info):
      import hashlib
      m = hashlib.md5()
      m.update(info)
      return m.hexdigest()

  @property
  def unique(self):
    return {'user_hash': self.user_hash}

  def __init__(self, cookie, uid=None):
    m = self.MD5Hash()
    self.user_hash = m.hexdigest(cookie)
    self.uid = uid

  def dict_to_db(self):
    return {
      'user_hash': self.user_hash,
      'uid': self.uid
    }

  def is_exists_and_registered(self):
    try:
      info = self.get_one_query(query=self.unique)
    except Exception, err:
      logger.info(err)
      return False, None

    else:
      return bool(info), info.get('uid', '')

  def register(self):
    if not self.uid:
      return

    self.update({'$set': {'uid': self.uid}})

  def get_uid(self):
    return self.uid if self.uid else self.user_hash