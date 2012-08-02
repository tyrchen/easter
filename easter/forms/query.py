# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
from django.utils import simplejson as json
from django import forms
from django.core import validators


class QueryForm(forms.Form):
  app_id = forms.CharField(max_length=30, min_length=5, label='app_id')
  app_token = forms.CharField(max_length=64, min_length=5, label='app_token')
  event = forms.CharField(max_length=30, label='event', validators=[validators.RegexValidator(re.compile(r'^[a-z][\w_]*$'))])
  query = forms.CharField(required=False, label='query', initial='{}')
  order_by = forms.CharField(required=False, label='order_by', initial='["-date"]')
  fields = forms.CharField(required=False, label='fields', initial='{"BASIC":""}')

  def __init__(self, data=None, request=None, *args, **kwargs):
    self.request = kwargs.pop('request', None)
    kwargs['data'] = data
    super(QueryForm, self).__init__(*args, **kwargs)

  def clean_query(self):
    err_msg = 'query field is invalid'
    data = self.cleaned_data['query']
    if not data:
      data = '{}'
    try:
      query = json.loads(data)
    except Exception:
      raise forms.ValidationError(err_msg)
    if isinstance(query, dict):
      pass #todo more check
    else:
      raise forms.ValidationError(err_msg)
    return query

  def clean_order_by(self):
    err_msg = 'order_by field is invalid'
    data = self.cleaned_data['order_by']
    if not data:
      data = '["-date"]'
    try:
      order_by = json.loads(data)
    except Exception:
      raise forms.ValidationError(err_msg)
    if isinstance(order_by, list):
      pass #todo more check
    else:
      raise forms.ValidationError(err_msg)
    return order_by

  def clean_fields(self):
    err_msg = 'fields field is invalid'
    data = self.cleaned_data['fields']
    if not data:
      data = '{"ALL":""}'
    try:
      fields = json.loads(data)
    except Exception:
      raise forms.ValidationError(err_msg)
    if isinstance(fields, dict):
      pass #todo more check
    else:
      raise forms.ValidationError(err_msg)
    return fields