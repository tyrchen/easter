# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.conf import settings
from datetime import datetime as py_time

THRESHOLD = settings.TIME_THRESHOLD or (72 * 3600)

def using_hours(from_datetime, to_datetime):
  delta = (to_datetime - from_datetime).total_seconds()
  if delta < THRESHOLD:
    return True
  else:
    return False

def total_num(item):
  if isinstance(item, dict):
    keys = filter(None, item.values())
    return sum(keys)
  else:
    return item

def document_datetime(date, hour):
  return py_time(year=date.year, month=date.month, day=date.day, hour=int(hour))

def to_datetime(str):
  return py_time.strptime(str, '%Y-%m-%d %H:%M:%S')

def datetime_to_str(datetime):
  return datetime.strftime('%Y-%m-%d %H:%M:%S')