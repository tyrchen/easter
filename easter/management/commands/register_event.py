# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.core.management.base import BaseCommand
from easter.collections import RegisteredEvents

"""
  例子：
  app_name = 'cayman'
  collection_name = 'event'

  record_time_fields = ['clip', 'board', 'clip__board']
  record_total_fields = ['total', {'origin': {'0': 'ipad', '1': 'web', '2': 'iphone'}}]
  unique_fields = ['date']
  fields_to_db = []
  event_pull_fields = ['text']
  alias = {'board': 'b', 'slug': 's', 'total': 't', 'iphone': 'i'}
  indexes = [(dict.fromkeys(unique_fields, 1), {'unique': True}), ]
"""

app_name = 'cayman'
event_name = 'create_clip'

record_time_fields = ['uid__board']
record_total_fields = ['total', {'origin': {'0': 'ipad', '1': 'web', '2': 'iphone'}}]
unique_fields = ['date']
fields_to_db = []
event_pull_fields = ['text']
alias = {'board': 'b', 'uid': 'u', 'total': 't', 'iphone': 'i', }
indexes = [(dict.fromkeys(unique_fields, 1), {'unique': True}), ]


class Command(BaseCommand):
  help = "通过配置来注册事件"

  def handle(self, *args, **options):
    r = RegisteredEvents(event_app=app_name, event_name=event_name, time_stat=record_time_fields,
                         total_stat=record_total_fields, event_unique=unique_fields, event_fields_to_db=fields_to_db,
                         event_fields_to_feeds=event_pull_fields, event_indexes=indexes, event_alias=alias)
    r.save()