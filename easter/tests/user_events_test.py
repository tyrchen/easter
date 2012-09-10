# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from easter.engines import UserEventsEngine, QueryGetEngine, EventPostEngine
import datetime
import random
from easter.utils.util import datetime_to_str
from easter.collections.event_register import RegisteredEvents
from easter.collections.user_events import UserEventFalls
from easter.collections.user_hash import UserHashTable
from easter.collections.events import EventFactory, EventHandler

ip = '127.0.0.1'
uid = 'simida'

delta_day = datetime.timedelta(days=1)
delta_hour = datetime.timedelta(hours=1)

now = datetime.datetime.now()
yesterday = now - delta_day
two_days_ago = now - delta_day*2
three_days_ago = now - delta_day*3
tomorrow = now + delta_day
two_days_later = now + delta_day*2
half_a_day_before = now - delta_hour*12

def show_all():
  def print_title(title):
    print("########%s#########" %title)

  register_events_collection = RegisteredEvents.get_collection()
  print_title("注册事件")
  for i in register_events_collection.find():
    print(i)

  user_hash_collection = UserHashTable.get_collection()
  print_title("用户hash表")
  for i in user_hash_collection.find():
   print(i)

  user_events_fall_collection = UserEventFalls.get_collection()
  print_title("用户事件流")
  for i in user_events_fall_collection.find():
    print(i)

  print_title("统计事件")
  for cluster in register_events_collection.find():
    cls_info = cluster
    format_data = RegisteredEvents.format_data(cls_info)
    event_handle = EventFactory.produce(format_data)
    collection = event_handle.get_collection()
    for i in collection.find():
      print(i)

def clear_all():
  def print_title(title):
    print("########%s#########" %title)

  register_events_collection = RegisteredEvents.get_collection()
  print_title("删除统计事件")
  for cluster in register_events_collection.find():
    cls_info = cluster
    format_data = RegisteredEvents.format_data(cls_info)
    event_handle = EventFactory.produce(format_data)
    event_handle.delete_all()

  print_title("删除用户事件流")
  UserEventFalls.delete_all()

  print_title("删除用户hash表")
  UserHashTable.delete_all()

  print_title("删除注册事件")
  RegisteredEvents.delete_all()

def random_user_info():
  user_list = [
    {'uid': 'chiyuan', 'cookie': 'chiyuan'},
    {'uid': 'gaopeng', 'cookie': 'simida'},
    {'uid': 'brian', 'cookie': 'naoge'},
    {'uid': 'tchen', 'cookie': 'tyr'}
  ]
  return random.choice(user_list)

def random_datetime():
  hour = random.choice(range(24))
  d = random.choice([two_days_ago, yesterday, now, tomorrow, two_days_later])
  d_time = datetime.datetime(year=d.year, month=d.month, day=d.day, hour=hour)
  return datetime_to_str(d_time)

def random_clip():
  return random.choice(['blue', 'yellow', 'green', 'black', 'white'])

def base_test():
  engine = UserEventsEngine()
  info = engine.execute(ip=ip, uid=None, from_datetime=yesterday, to_datetime=now)
  for i in info:
    print(i)

def post_test():
  engine = EventPostEngine()
  user_info = random_user_info()
  events = [{
    'event_name': 'create_clip',
    'clip':  random_clip(),
    'datetime': random_datetime()
  }]
  engine.execute(sig='ss', app_name='cayman', user_info=user_info, events=events)

def query_test(from_datetime=2, to_datetime=2):
  now = datetime.datetime.now()
  engine = QueryGetEngine()
  query = {
    'event_name': 'create_clip',
    'from_datetime': datetime_to_str(now - delta_day*from_datetime),
    'to_datetime': datetime_to_str(now + delta_day*to_datetime)
  }
  fields = [{
    'uid': 'chiyuan',
    'clip': 'blue'
  }]
  info = engine.execute(ip=ip, app_name='cayman', query=query, fields=fields)
  return info