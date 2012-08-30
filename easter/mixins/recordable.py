# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from mongoable import Mongoable

class BaseRecord(Mongoable):
  def record(self):
    exists = self.exists()
    if not exists:
      self.save()

    update_dict = self.update_objs()
    if not update_dict:
      return

    self.update(obj=update_dict)
    self.after_update()

  def update_objs(self):
    return {}

  def after_update(self):
    pass