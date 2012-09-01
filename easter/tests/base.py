# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from datetime import datetime as py_time
from easter.engines import EventPostEngine
from easter.collections import (UserEventFalls, UserHashTable,
                           EventHandler, RegisteredEvents)

import time
import md5
import json

POST_URL = 'http://127.0.0.1:8009/api/v1/event/'
engine = EventPostEngine()

app_name = 'cayman'
collection_name = 'create_clip'
db_info = {
  'app_name': app_name,
}

anonymous_simida = {'uid': '', 'cookie': 'kimgee'}
simida = {'uid': 'simida', 'cookie': 'kimgee'}

event1 = {'event_name': collection_name, 'board': 'board1', 'origin': '1',
          'text': 'I love zixiao', 'datetime': py_time.now().strftime('%Y-%m-%d %H:%M:%S')}

time.sleep(0.1)

event2 = {'collection_name': collection_name, 'clip': 'clip2', 'board': 'board2', 'origin': '2',
          'text': 'Zixiao, do you love me?', 'datetime': py_time.now().strftime('%Y-%m-%d %H:%M:%S')}

time.sleep(0.1)

event3 = {'collection_name': collection_name, 'clip': 'clip3', 'board': 'board3', 'origin': '2',
          'text': 'Zixiao, We are in love'}

def show_all():
  print('注册事件表')
  rigister_event_collection = RegisteredEvents.get_collection()
  for r_event in rigister_event_collection.find():
    print(r_event)

  user_event_collection = UserEventFalls.get_collection()
  print("\n用户的事件流数据")
  for user_event in user_event_collection.find():
    print(user_event)

  user_hash_collection = UserHashTable.get_collection()
  print('\n哈希表数据')
  for user_hash in user_hash_collection.find():
    print(user_hash)

  print('\n事件记录表')
  event_collection = EventHandler.get_collection()
  for event in event_collection.find():
    print(event)

def clear_all():
  print("清除用户的事件流数据")
  UserEventFalls.delete_all()
  print('清除哈希表数据')
  UserHashTable.delete_all()
  print('清除事件记录表')
  EventHandler.delete_all()
  print("清除注册事件")
  RegisteredEvents.delete_all()

def event_test():
  e = EventHandler(collection_name, uid='gaopeng', **event1)
  e.record()
  show_all()

def smart_sig(app_name, user_info, events=[]):
  json_data = {
    'app_name': app_name,
    'user_info': user_info,
    'events': events
  }
  m = md5.new(json.dumps(json_data))
  sig = m.hexdigest()
  return sig

def base_test():
  print("###"*10)
  print("高鹏匿名发了一条event")
  sig = smart_sig(app_name, anonymous_simida, [event1, ])
  engine.execute(sig, app_name, user_info=anonymous_simida, events=[event1,])
  show_all()
  print("###"*10)

  print("高鹏现身了，此时的数据")
  sig = smart_sig(app_name, simida, [event2, event3])
  engine.execute(sig, app_name, user_info=simida, events=[event2, event3])
  show_all()
  print("###"*10)

  print("将他们的数据merge之后")
  user_hash_collection = UserHashTable.get_collection()
  user_info = user_hash_collection.find()[0]
  UserEventFalls.merge(from_uid=user_info['user_hash'], to_uid=user_info['uid'])
  show_all()

def register_events_test():
  app_name = 'cayman'
  collection_name = 'event'

  record_time_fields = ['clip', 'board', 'clip__board']
  record_total_fields = ['total', {'origin': {'0': 'ipad', '1': 'web', '2': 'iphone'}}]
  unique_fields = ['date']
  fields_to_db = []
  event_pull_fields = ['text']
  alias = {'board': 'b', 'slug': 's', 'total': 't', 'iphone': 'i'}
  indexes = [(dict.fromkeys(unique_fields, 1), {'unique': True}), ]

  r = RegisteredEvents(event_app=app_name, event_collection=collection_name, time_stat=record_time_fields,
                       total_stat=record_total_fields, event_unique=unique_fields, event_fields_to_db=fields_to_db,
                       event_fields_to_feeds=event_pull_fields, event_indexes=indexes, event_alias=alias)
  r.save()

  json_data = RegisteredEvents.get_by_name(event_app=app_name, event_collection=collection_name)
  print(json_data)

def md5_sig(json_data):
  m = md5.new(json.dumps(json_data))
  sig = m.hexdigest()
  return sig

def post(app_name, user_info, events):
  """
      Post event data to log server.
      :Params app_name str: The register app name.
      :Params user_info dict:  It contains uid & cookie. Like {'uid': 'ccy', 'cookie': 'abcdef'}
      :Params events list: It contains event info, likes event_name, origin, text, datetime etc
      @return status_code: Like 200, 400, 403, 404, same as Http response status.
    """
  import requests
  json_data = {
      'app_name': app_name,
      'user_info': user_info,
      'events': events
    }
  sig = md5_sig(json_data)
  info = {
      'sig': sig,
      'app_name': app_name,
      'user_info': json.dumps(user_info),
      'events': json.dumps(events)
  }

  headers = {'content-type': 'application/json'}
  r = requests.post(url=POST_URL, data=json.dumps(info), headers=headers)
  return r.status_code

def http_test():
  json_data = {
    'app_name': app_name,
    'user_info': anonymous_simida,
    'events': [event1,]
  }
  m = md5.new(json.dumps(json_data))
  sig = m.hexdigest()
  json_data.update({'sig': sig})

  post(app_name, simida, [event1])