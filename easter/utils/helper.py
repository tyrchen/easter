# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

def merge_dicts(*dicts):
  if isinstance(dicts[0], (int, float)):
    return sum(dicts)

  result = {}
  for dict in dicts:
    for key in dict:
      if not result.has_key(key):
        result[key] = dict[key]
      else:
        merged_dict = merge_dicts(result[key], dict[key])
        result[key] = merged_dict
  return result
  