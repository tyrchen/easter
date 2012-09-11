# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from collections import (UserHashTable, EventHandler, RegisteredEvents,
                         UserEventFalls, EventFactory)
from utils.exceptions import InfoIllegalException, SignitureException
from easter.core.interpreter import QueryInterpreter
from core.verification import Verification
from datetime import datetime as py_time
from utils.util import datetime_to_str

import json
import logging

logger = logging.getLogger(__name__)

class EventPostEngine(object):
  """
  处理过来的请求，可以认为是业务逻辑。
  TODO：考虑更好的抽象。
  """
  def execute(self, sig, app_name, user_info, events=[]):
    """
      执行逻辑，抛出异常，丢给执行端处理。
      动态添加验证方法。
    """
    json_data = {
      'app_name': app_name,
      'user_info': user_info,
      'events': events
      }
    v = Verification()

    try:
      validate = all([v.verify_info(sig, json_data),])
    except Exception, err:
      logger.info(err)
      raise InfoIllegalException("参数不合法")

    if not validate:
      raise SignitureException("签名验证失败")

    try:
      self.do_events(app_name, user_info, events)
    except Exception:
      raise InfoIllegalException("参数不合法")

  def do_events(self, app_name, user_info, events=[]):
    uid = self.authentication(user_info)

    for event in events:
      collection_name = event.get('event_name', '')
      cls_info = RegisteredEvents.get_by_name(app_name, collection_name)
      self.do_event(cls_info=cls_info, uid=uid, event=event)

  def do_event(self, uid, cls_info, event):
    """
      对于每个事件的处理，实际调用了collection的record行为。
    """
    handle = EventFactory.produce(cls_info)
    instance = handle(uid=uid, **event)
    instance.record()

  def authentication(self, user_info):
    cookie = user_info['cookie']
    uid = user_info.get('uid', '')

    u_hash = UserHashTable(cookie=cookie, uid=uid)
    exists, user_id = u_hash.is_exists_and_registered()

    if not exists:
      u_hash.save()
    if not user_id:
      u_hash.register()

    if not uid and user_id:
      u_hash.uid = user_id

    return u_hash.get_uid()

class QueryGetEngine(object):
  def execute(self, ip, app_name, query, fields, **kwargs):
    v = Verification()
    try:
      validate = all([v.verify_ip(ip), ])
    except Exception, err:
      logger.info(err)
      raise InfoIllegalException("参数不合法")

    if not validate:
      raise SignitureException("签名验证失败")

    try:
      info = self.do_query(app_name, query, fields, **kwargs)
    except Exception, err:
      logger.info(err)
      raise InfoIllegalException("参数不合法")
    else:
      return info

  def do_query(self, app_name, query, fields, **kwargs):
    collection_name = query.pop('event_name', '')
    from_datetime = query.pop('from_datetime', '')
    to_datetime = query.pop('to_datetime', '')

    cls_info = RegisteredEvents.get_by_name(app_name, collection_name)

    alias = cls_info['alias']
    key_fields = QueryInterpreter.parse(fields, alias)

    handle = EventFactory.produce(cls_info)
    info = handle.mget(from_datetime=from_datetime,
                             to_datetime=to_datetime, fields=key_fields)
    return info

class UserEventsEngine(object):
  def execute(self, ip, uid=None, from_datetime=py_time.now(), to_datetime=py_time.now()):
    v = Verification()
    try:
      validate = all([v.verify_ip(ip), ])
    except Exception, err:
      logger.info(err)
      raise InfoIllegalException("参数不合法")

    if not validate:
      raise SignitureException("签名验证失败")

    try:
      info = self.do_query(uid, from_datetime, to_datetime)
    except Exception, err:
      logger.info(err)
      raise InfoIllegalException("参数不合法")
    else:
      return info

  def do_query(self, uid=None, from_datetime=py_time.now(), to_datetime=py_time.now()):
    info = UserEventFalls.get(uid, from_datetime, to_datetime)
    for item in info:
      item['datetime'] = datetime_to_str(item['datetime'])
    return info