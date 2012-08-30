# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

def keys_format(alias={}, **kwargs):
  sorted_items = sorted(kwargs.iteritems(), key=lambda x: x[1])
  items = []
  for key, value in sorted_items:
    if not value:
      if alias.has_key(key):
        key = alias[key]
      items.append(key)

    else:
      if alias.has_key(key):
        key = alias[key]
      items.append(key + '_' + str(value))
  return '#'.join(items)

class StatTemplateInterpreter(object):
  """
  这里应该通过给出的模板，分析出记录的可以的形式。而具体的记录行为，应该不管
  """
  @classmethod
  def parse(cls, instance, field_list, alias={}):
    d = []
    for item in field_list:
      if isinstance(item, dict):
        for key in item:
          field = cls.do_condition_filter(instance, key, item[key])
          if alias.has_key(field):
            field = alias[field]
          d.append(field)
      else:
        key_dict = cls.do_key_explain(instance, item)
        d.append(keys_format(alias=alias, **key_dict))
    return list(set(d))

  @classmethod
  def do_condition_filter(cls, instance, key, condition):
    value = cls.get_value(instance, key)
    return condition[value]

  @classmethod
  def do_key_explain(cls, instance, key):
    """
      Key likes a__b, a.c__b ....
    """
    keys = key.split('__')
    dict = {}
    for key in keys:
      value = cls.get_value(instance, key)
      dict[key] = value
    return dict

  @classmethod
  def get_value(cls, instance, key):
    embedded_fields = key.split('.')
    field = embedded_fields.pop(0)
    if not hasattr(instance, field):
      return None

    value = getattr(instance, field)
    for hash_field in embedded_fields:
      value = value.get(hash_field, '')
    return value

class QueryInterpreter(object):
  @classmethod
  def parse(cls, field_list, alias={}):
    key_lists = []
    for field in field_list:
      if isinstance(field, dict):
        key_lists.append(keys_format(alias=alias, **field))
      else:
        key_lists.append(keys_format(alias=alias, **{field: None}))
    return key_lists

  


