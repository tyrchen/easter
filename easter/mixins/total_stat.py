# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

import logging

logger = logging.getLogger(__file__)

class TotalStatistics:
  def total_record_fields(self):
    raise NotImplemented

  def total_record(self):
    update_fields_dict = {}
    recode_fields = self.total_record_fields()
    for field in recode_fields:
      update_fields_dict.update({
        field: 1
      })

    if not update_fields_dict:
      return {}
    
    return {"$inc": update_fields_dict}