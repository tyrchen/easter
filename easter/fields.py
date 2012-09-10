# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.db import models

import json
from django.utils.encoding import smart_unicode

class JsonField(models.TextField):
  __metaclass__ = models.SubfieldBase

  def __init__(self, *args, **kwargs):
    kwargs['default'] = kwargs.get('default', '')
    super(JsonField, self).__init__(*args, **kwargs)

  def to_python(self, value):
    if not value:
      return
    if isinstance(value, basestring):
      return json.loads(value, encoding='utf-8')
    else:
      return value

  def get_prep_value(self, value):
    if not value:
      return
    assert isinstance(value, list) or isinstance(value, dict)
    return json.dumps(value, encoding='utf-8')

class SeparatedValuesField(models.TextField):
  __metaclass__ = models.SubfieldBase

  def __init__(self, *args, **kwargs):
    kwargs['default'] = kwargs.get('default', '')
    self.token = kwargs.pop('token', ',')
    super(SeparatedValuesField, self).__init__(*args, **kwargs)

  def to_python(self, value):
    if not value:
      return
    if isinstance(value, list):
      return value
    return value.split(self.token)

  def get_prep_value(self, value):
    if not value:
      return
    assert(isinstance(value, list) or isinstance(value, tuple))
    return self.token.join([smart_unicode(s) for s in value])

  def value_to_string(self, obj):
    value = self._get_val_from_obj(obj)
    return self.get_prep_value(value)