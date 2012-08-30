# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

class EventPushAble:
  def pushable_fields(self):
    raise NotImplemented

  def push_record(self):
    result = {}
    fields = self.pushable_fields()

    for field in fields:
      result[field] = getattr(self, field, '')

    return {"$push": {'events': result}}