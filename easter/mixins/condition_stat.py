# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

import logging

logger = logging.getLogger(__file__)

class ConditionStatistics:
  def condition_record_fields(self):
    raise NotImplemented

  def condition_record(self):
    update_fields_dict = {}
    recode_fields = self.condition_record_fields()
    for field in recode_fields:
      for key, value in field.items():
        field = value[getattr(self, key)]
        update_fields_dict[field] = update_fields_dict.get('field', 0) + 1

    if not update_fields_dict:
      return {}
    
    return {"$inc": update_fields_dict}