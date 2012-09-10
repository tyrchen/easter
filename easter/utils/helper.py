# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from easter.utils.util import datetime_to_str
from datetime import datetime as py_time
from datetime import timedelta

def merge_dicts(*dicts):
  if isinstance(dicts[0], (int, float)):
    return sum(dicts)

  result = {}
  for dict in dicts:
    for key in dict:
      if not result.has_key(key):
        result[key] = dict[key]
      else:
        merged_dict = merge_dicts(result[key], dict[key])
        result[key] = merged_dict
  return result

def time_dict(from_datetime, to_datetime, using='hour', blank=0):
  """
  分发时间处理函数
  """
  distribute_dict = {
    'hours': delta_hour_dict,
    'days': delta_day_dict
  }
  handler = distribute_dict[using]
  return handler(from_datetime, to_datetime, blank)

def delta_hour_dict(from_datetime, to_datetime, blank=0):
  """
  以小时为维度处理时间，默认值为0
  """
  delta_hours = 1

  hours = {
    datetime_to_str(to_datetime): blank,
    datetime_to_str(from_datetime): blank
  }

  while True:
    datetime = from_datetime + timedelta(hours=delta_hours)
    if datetime > to_datetime:
      break
    else:
      hours.update({
        datetime_to_str(datetime): blank
      })
    delta_hours += 1
  return hours

def delta_day_dict(from_datetime, to_datetime, blank=0):
  """
  以天为维度处理时间，默认值为0
  """
  start_day = py_time(year=from_datetime.year, month=from_datetime.month,
                      day=from_datetime.day)
  end_day = py_time(year=to_datetime.year, month=to_datetime.month, day=to_datetime.day)

  time_deltas = end_day - start_day
  days = {}
  for day in range(time_deltas.days+1):
    if day == 0:
      datetime = from_datetime
    elif day == time_deltas.days:
      datetime = to_datetime
    else:
      datetime = start_day + timedelta(days=day)
    days.update({
      datetime_to_str(datetime): blank
    })
  return days