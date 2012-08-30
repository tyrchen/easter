# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from djangorestframework.views import View
from utils.http import http_400, http_403, http_200, json_response
from engines import EventPostEngine, QueryGetEngine, UserEventsEngine

import json
import logging

logger = logging.getLogger(__name__)

class EventView(View):
  def post(self, request, *args, **kwargs):
    info = self.CONTENT

    try:
      sig = info.get('sig', '')
      app_name = info.get('app_name', '')
      user_info = json.loads(info.get('user_info', {}))
      events = json.loads(info.get('events', {}))
    except Exception, err:
      logger.info(err)
      return http_400()

    engine = EventPostEngine()
    try:
      engine.execute(sig, app_name, user_info, events)
    except Exception, err:
      logger.info(err)
      return http_403()

    return http_200()

  def get(self, request, *args, **kwargs):
    ip = request.META['REMOTE_ADDR']
    app_name = request.GET.get('app_name', '')
    query = request.GET.get('query', '')
    fields = request.GET.get('fields', '')

    try:
      query = json.loads(query)
      fields = json.loads(fields)
    except Exception, err:
      logger.info(err)
      return http_400()

    engine = QueryGetEngine()
    try:
      info = engine.execute(ip, app_name, query, fields)
    except Exception:
      return http_403()

    return json_response(info)

class UserEventsView(View):
  def get(self, request, *args, **kwargs):
    ip = request.META['REMOTE_ADDR']
    uid = request.GET.get('uid', '')
    from_datetime = request.GET.get('from_datetime', '')
    to_datetime = request.GET.get('to_datetime', '')

    engine = UserEventsEngine()
    try:
      info = engine.execute(ip, uid, from_datetime, to_datetime)
    except Exception, err:
      logger.info(err)
      return http_403()

    return json_response(info)




      