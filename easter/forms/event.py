# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re
from django.utils import simplejson as json
from django import forms
from django.core import validators


class EventForm(forms.Form):
  app_id = forms.CharField(max_length=30, min_length=5, label='app_id')
  time = forms.FloatField(label='time', max_value=2<<30)
  event = forms.CharField(max_length=30, label='event', validators=[validators.RegexValidator(re.compile(r'^[a-z][\w_]*$'))])
  uid = forms.CharField(label='uid', required=False, initial='')
  origin = forms.IntegerField(min_value=0, required=False, initial=0, label='origin')
  level = forms.IntegerField(min_value=0, required=False, initial=0, label='level')
  text = forms.CharField(required=False, label='text', initial='')
  data = forms.CharField(required=False, label='data', initial='{}')

  def __init__(self, data=None, request=None, *args, **kwargs):
    self.request = kwargs.pop('request', None)
    kwargs['data'] = data
    super(EventForm, self).__init__(*args, **kwargs)

  def clean_data(self):
    data = self.cleaned_data['data']
    if not data:
      data = '{}'
    try:
      ret = json.loads(data)
    except Exception:
      raise forms.ValidationError('data field is invalid')
    return ret

#  def clean_uid(self):
#    pass