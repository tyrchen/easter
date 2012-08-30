# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)

import json

def json_response(info):
  return HttpResponse(json.dumps(info),
          mimetype='application/json')

def http_200():
  return json_response({'ret': 200})

def http_400():
  return HttpResponseBadRequest()

def http_403():
  return HttpResponseForbidden()


