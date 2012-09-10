# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

import logging
from django.db import models
from fields import JsonField, SeparatedValuesField
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)

class Event(models.Model):
  """
  事件的Django Model，目的只是为了admin.
  TODO：1. after save事件的处理。
        2. 处理注册很困难的问题。
  """
  class Meta:
    unique_together = ('app_name', 'collection_name')

  app_name = models.CharField(max_length=32, verbose_name=u'应用名称')
  collection_name = models.CharField(max_length=32, verbose_name=u'集合名称')
  unique_fields = SeparatedValuesField()
  indexes = JsonField()

  event_pull_fields = SeparatedValuesField()
  record_time_fields = SeparatedValuesField()
  record_total_fields = JsonField()
  alias = JsonField()

def after_event_save(sender, **kwargs):
  print("Event save signal")

post_save.connect(after_event_save, sender=Event)
  
