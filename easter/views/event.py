# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils import simplejson as json
from djangorestframework.views import View
from djangorestframework.response import Response
from djangorestframework import status
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pymongo import Connection
from easter.forms.event import EventForm

import logging
from datetime import datetime

from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)

err_codes = {
  0: 'ok',
  1: 'invalid params',
  2: 'missing required param(s)',
  3: 'app does not exist',
  4: 'event quota exceeded',  #todo
}

class CodeResponse(Response):
  def __init__(self, code=0, status=status.HTTP_200_OK, headers=None):
    content = {'code': code, 'msg': err_codes.get(code, '')}
    super(CodeResponse, self).__init__(status, content, headers)

class EventView(View):
  con = Connection()

  def post(self, request):
    data = json.loads(request.raw_post_data)
    code, cleaned_data = self.format_check(data, request)
    if code:
      return CodeResponse(code=code)
    for form in cleaned_data:
      code = self.do_event(request, form)
      if code:
        return CodeResponse(code=code)

    return CodeResponse(code=0)

  def get(self, request):
    return CodeResponse()

  def do_event(self, request, form):
    app_id = form['app_id']
    event = form['event']
    c_time = form['time']
    if not app_id in self.con.database_names():
      return 3
    db = self.con[app_id]
    collections = db[event]
    s_time = datetime.now()
    date = s_time.replace(hour=0, minute=0, second=0, microsecond=0)
    hour = s_time.hour
    spec = {'user': form['uid'], 'date': date}
    fields = dict.fromkeys(['hour.%s' % hour, 'total.TOTAL', 'total.%s' % form['origin']], 1)
    fields.update(self._build_ops_fields(form['data']))
    ops = {'$inc' : fields}
    collections.update(spec, ops, True)
    spec['user'] = 'ALL'
    collections.update(spec, ops, True)

    if form['level'] > 0 and form['text']:
      event_collections = db._event
      _event = {
        'user': form['uid'],
        'ctime': datetime.fromtimestamp(c_time),
        'stime': s_time,
        'event': event,
        'origin': form['origin'],
        'level': form['level'],
        'text': form['text']
      }
      event_collections.insert(_event)


  def _build_ops_fields(self, data):
    fields = {}
    for f, v in data.items():
      if isinstance(v, list):
        fields.update(dict.fromkeys(['%s.%s' % (f, item) for item in v], 1))
        fields['%s.%s' % (f, 'TOTAL')] = len(v)
      else:
        fields['%s.%s' % (f, v)] = 1
        fields['%s.%s' % (f, 'TOTAL')] = 1
    return fields



  def set_cookie(self, response, key, value, days_expire=7):
    if days_expire:
      max_age = days_expire * 86400  #24 * 60 * 60
    else:
      max_age = 365 * 86400
    response.set_cookie(key, value, max_age=max_age)

  def __format_check_deprecated(self, data):
    """
    check params format, and return (ok_or_not, cleaned data)
    """
    cleaned_data = []
    if not isinstance(data, list):
      return 0, []
    required_fields = dict.fromkeys(['app_id', 'time', 'event'])
    optional_fields = {'uid': '', 'origin': 1, 'level': 0, 'text': '', 'data': {}}
    formats = {
      'app_id': lambda x: isinstance(x, basestring),
      'time': lambda x: isinstance(x, float),
      'event': lambda x: isinstance(x, basestring) and len(x) <=30,
      'uid': lambda x: isinstance(x, basestring),
      'origin': lambda x: isinstance(x, int) and 1<=x<=5,
      'level': lambda x: isinstance(x, int) and 0<=x<=9,
      'text': lambda x: isinstance(x, basestring),
      'data': lambda x: isinstance(x, dict),
    }
    for info in data:
      if not isinstance(info, dict):
        return 0, 0
      absent_fields = required_fields.copy()
      cleaned_info = {}
      try:
        for param, value in info.items():
          if param in formats:
            if not formats[param](value):
              return 0, 0

          cleaned_info[param] = value
          if param in required_fields:
            absent_fields.pop(param)
        if absent_fields:
          return 0, 1
        else:
          cleaned_data.append(cleaned_info)
      except Exception:
        return 0, 0
    return 1, cleaned_data

  def format_check(self, data, request):
    cleaned_data = []
    if not isinstance(data, list):
      return 1, 0
    for info in data:
      if not isinstance(info, dict):
        return 1, 0
      _data = info.get('data')
      if _data:
        info['data'] = json.dumps(_data).lower()
      form = EventForm(info, request)
      if not form.is_valid():
        return 1, 0
      else:
        cleaned_data.append(form.cleaned_data)
    return 0, cleaned_data

class TestClientView(TemplateView):
  template_name = 'demo_client.html'

#  @method_decorator(login_required)
#  def dispatch(self, request, *args, **kwargs):
#    return super(EventView, self).dispatch(request, *args, **kwargs)