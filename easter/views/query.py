# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils import simplejson as json
from djangorestframework.views import View
from pymongo import Connection
from easter.forms.query import QueryForm
from easter.views.code_response import CodeResponse

import logging

logger = logging.getLogger(__name__)

class QueryView(View):
  con = Connection()

  def post(self, request):
    data = json.loads(request.raw_post_data)
    code, cleaned_data = self.format_check(data, request)
    if code:
      return CodeResponse(code=code)

    code = self.do_query(cleaned_data)
    return CodeResponse(code=code)

  def do_query(self, data):
    return 0


  def format_check(self, data, request):
    if not isinstance(data, dict):
      return 200, 0
    to_do = ('query', 'order_by', 'fields')
    for field in to_do:
      _data = data.get(field)
      if _data:
        data[field] = json.dumps(_data)
    form = QueryForm(data, request)
    if not form.is_valid():
      return 200, 0
    return 0, form.cleaned_data