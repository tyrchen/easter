# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from easter.models import Event

app_name = 'cayman'
collection_name = 'event'

record_time_fields = ['clip', 'board', 'clip__board']
record_total_fields = ['total', {'origin': {'0': 'ipad', '1': 'web', '2': 'iphone'}}]
unique_fields = ['date']
fields_to_db = []
event_pull_fields = ['text']
alias = {'board': 'b', 'slug': 's', 'total': 't', 'iphone': 'i'}
indexes = [(dict.fromkeys(unique_fields, 1), {'unique': True}), ]

def test():
  e = Event(app_name=app_name, collection_name=collection_name, record_time_fields=record_time_fields,
            record_total_fields=record_total_fields, unique_fields=unique_fields, event_pull_fields=event_pull_fields,
            alias=alias, indexes=indexes)
  try:
    e.save()
  except Exception, err:
    print(err)