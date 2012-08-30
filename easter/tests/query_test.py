# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from easter.collections import UserEventFalls
from easter.engines import QueryGetEngine

import datetime
import json

app_name = 'cayman'
collection_name = 'event'

delta_day = datetime.timedelta(days=1)
delta_hour = datetime.timedelta(hours=1)

now = datetime.datetime.now()
yesterday = now - delta_day
two_days_ago = now - delta_day*2
three_days_ago = now - delta_day*3
tomorrow = now + delta_day
two_days_later = now + delta_day*2
half_a_day_before = now - delta_hour*12

def show_cursors(cursors):
  for data in cursors:
    print(data)

def datetime_to_date(d):
  return datetime.datetime(year=d.year, month=d.month, day=d.day)

def event_poll_query():
  all_cursor = UserEventFalls.get(uid='simida', min=half_a_day_before, max=tomorrow)
  show_cursors(all_cursor)

  only_text = UserEventFalls.get(uid='simida', min=half_a_day_before,
                                 max=tomorrow, only=['text'])
  show_cursors(only_text)

def event_days_query():
  from_date = three_days_ago
  to_date = two_days_later
  query = {
    'collection_name': collection_name,
    'from_datetime': from_date,
    'to_datetime': to_date,
  }
  engine = QueryGetEngine()
  engine.execute(ip='127.0.0.1', app_name=app_name, query=query, fields=[{'board': 'board1', 'clip': 'clip2'},])

def event_hours_query():
  from_date = yesterday
  to_date = now
  query = {
    'collection_name': collection_name,
    'from_datetime': from_date,
    'to_datetime': to_date,
  }
  engine = QueryGetEngine()
  info = engine.execute(ip='127.0.0.1', app_name=app_name, query=query, fields=[{'board': 'board1', 'clip': 'clip2'},])
  for i in info:
    print(i)

def http_test():
  from_date = yesterday
  to_date = now
  query = {
    'collection_name': collection_name,
    'from_datetime': from_date.strftime('%Y-%m-%d %H:%M:%S'),
    'to_datetime': to_date.strftime('%Y-%m-%d %H:%M:%S'),
  }
  query = json.dumps(query)
  fields = json.dumps([{'board': 'board1', 'clip': 'clip2'},])
  params = {
    'app_name': app_name,
    'query': query,
    'fields': fields
  }
  
  import requests
  r = requests.get(url='http://127.0.0.1:8000/api/v1/event/', params=params)
  print(r.content)