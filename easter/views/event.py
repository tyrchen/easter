# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid
from django.utils import simplejson as json
from djangorestframework.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pymongo import Connection
from easter.forms.event import EventForm
from easter.views.code_response import CodeResponse

import logging
from datetime import datetime

from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)

class EventView(View):
  con = Connection()

  def post(self, request):
    data = json.loads(request.raw_post_data)
    code, cleaned_data = self.format_check(data, request)
    if code:
      return CodeResponse(code=code)
    hid, new_tid = self.record_user(request, cleaned_data)
    code = self.do_event(cleaned_data, hid)
    return CodeResponse(code=code, new_tid=new_tid)

  def final(self, request, response, *args, **kwargs):
    new_tid = response.new_tid
    response = super(EventView, self).final(request, response, *args, **kwargs)
    if request.method == 'POST':
      tid = new_tid or request.COOKIES.get('tid')
      if tid:
        response.set_cookie(str('tid'), tid, max_age=86400)  #expire in a day
    return response

  def record_user(self, request, form):
    app_id = form['app_id']
    uid = form.get('uid', '')
    tid = request.COOKIES.get('tid', '')
    new_tid = ''
    if not tid:
      new_tid = uuid.uuid4().hex
    ip = self.get_client_ip(request)

    db = self.con[app_id]
    users = db._users
    hid = self.build_hid(ip, tid or new_tid)
    if uid:
      users.update({'hid': hid}, {'$set': {'cookie': tid, 'ip': ip, 'uid': uid}}, upsert=True)
    else:
      users.update({'hid': hid}, {'$set': {'cookie': tid or new_tid, 'ip': ip}}, upsert=True)
    return hid, new_tid

  def build_hid(self, ip, tid):
    return ':'.join([tid, ip]) if tid or ip else ''

  def get_client_ip(self, request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
      ip = x_forwarded_for.split(',')[0]
    else:
      ip = request.META.get('REMOTE_ADDR', '')
    return ip

  def do_event(self, form, hid):
    uid = form.get('uid', '')
    app_id = form['app_id']
    event = form['event']
    c_time = form['time']
    if not app_id in self.con.database_names():
      return 101
    db = self.con[app_id]
    collections = db[event]
    s_time = datetime.now()
    date = s_time.replace(hour=0, minute=0, second=0, microsecond=0)
    hour = s_time.hour
    if uid:
      spec = {'uid': uid, 'date': date}
    elif hid:
      spec = {'hid': hid, 'date': date}
    else:
      return 0
    fields = dict.fromkeys(['hour.%s' % hour, 'total.TOTAL', 'total.%s' % form['origin']], 1)
    fields.update(self._build_ops_fields(form['data']))
    ops = {'$inc' : fields}
    collections.update(spec, ops, True)
    spec = {'hid': 'ALL', 'date': date}
    collections.update(spec, ops, True)

    if form['level'] > 0 and form['text']:
      event_collections = db._event
      _event = {
        'uid': uid,
        'hid': hid,
        'ctime': datetime.fromtimestamp(c_time),
        'stime': s_time,
        'event': event,
        'origin': form['origin'],
        'level': form['level'],
        'text': form['text']
      }
      event_collections.insert(_event)
    return 0


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

  def format_check(self, data, request):
    if not isinstance(data, dict):
      return 200, 0
    _data = data.get('data')
    if _data:
      data['data'] = json.dumps(_data).lower()
    form = EventForm(data, request)
    if not form.is_valid():
      return 200, 0
    return 0, form.cleaned_data

class TestClientView(TemplateView):
  template_name = 'demo_client.html'

#  @method_decorator(login_required)
#  def dispatch(self, request, *args, **kwargs):
#    return super(EventView, self).dispatch(request, *args, **kwargs)