# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from datetime import datetime as py_time
import logging

logger = logging.getLogger(__file__)

class TimeStatistics:
  def time_recode_field_format(self, field, datetime=py_time.now()):
      hour = str(datetime.hour)
      return "%s.%s" %(field, hour)

  def time_record_fields(self):
    raise NotImplemented

  def time_record(self, datetime=py_time.now()):
    update_fields_dict = {}
    recode_fields = self.time_record_fields()
    for field in recode_fields:
      name = self.time_recode_field_format(field, datetime)
      if not name:
        continue

      update_fields_dict.update({
        name: 1
      })
    if not update_fields_dict:
      return {}
    
    return {"$inc": update_fields_dict}
