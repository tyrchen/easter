# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.core.management.base import BaseCommand
from easter.collections import RegisteredEvents

import copy

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

unique_fields = ['date']
alias = {'board': 'b', 'uid': 'u', 'total': 't', 'iphone': 'i', }
indexes = [(dict.fromkeys(unique_fields, 1), {'unique': True}), ]

alias = {'board': 'b', 'uid': 'u', 'total': 't', 'iphone': 'i', 'clip': 'c'}

BASE_INFO = {
  'event_app': 'cayman',
  'total_stat': [{'origin': {'0': 'web', '1': 'iphone', '2': 'ipad'}}],
  'event_unique': ['date'],
  'event_fields_to_db': [],
  'event_fields_to_feeds': ['text'],
  'event_indexes': [(dict.fromkeys(unique_fields, 1), {'unique': True}), ],
  'event_alias': alias
}

register_list = [{
  'event_name': 'like_clip', #喜欢clip
  'time_stat': ['uid__clip'],
  }, {
  'event_name': 'unlike_clip', #不喜欢clip
  'time_stat': ['uid__clip']
  }, {
  'event_name': 'like_board',  #喜欢board
  'time_stat': ['uid__board'],
  }, {
  'event_name': 'unlike_board', #不喜欢board
  'time_stat': ['uid__board'],
  }, {
  'event_name': 'share_clip', #分享clip
  'time_stat': ['uid__clip'],
  }, {
  'event_name': 'share_board', #分享board
  'time_stat': ['uid__board'],
  }, {
  'event_name': 'repost_clip', #repost clip
  'time_stat': ['uid__clip'],
  },{
  'event_name': 'create_clip',   #新建clip
  'time_stat': ['uid__board'],
  }, {
  'event_name': 'modify_clip', #修改clip
  'time_stat': ['uid__clip'],
  }, {
  'event_name': 'delete_clip', #删除clip
  'time_stat': ['uid__clip'],
  }, {
  'event_name': 'repost_clip', #repost clip
  'time_stat': ['uid__clip'],
  },  {
  'event_name': 'create_board',   #新建board
  'time_stat': ['uid'],
  }, {
  'event_name': 'modify_board', #修改board
  'time_stat': ['uid__board'],
  }, {
  'event_name': 'delete_board', #删除board
  'time_stat': ['uid__board'],
  },
]

class Command(BaseCommand):
  help = "通过配置来注册事件"

  def handle(self, *args, **options):
    for event in register_list:
      base = copy.deepcopy(BASE_INFO)
      base.update(event)
      r = RegisteredEvents(**base)
      r.save()