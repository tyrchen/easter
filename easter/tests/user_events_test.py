# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from easter.engines import UserEventsEngine
import datetime

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

def base_test():
  engine = UserEventsEngine()
  info = engine.execute(ip=ip, uid=None, from_datetime=yesterday, to_datetime=now)
  for i in info:
    print(i)