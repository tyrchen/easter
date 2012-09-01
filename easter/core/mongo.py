# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.conf import settings

import pymongo
import logging

logger = logging.getLogger(__file__)

connection = pymongo.Connection(host=settings.MONGO_HOST, port=settings.MONGO_PORT)

def get_mongodb(app_name):
  assert bool(app_name) == True
  return connection[app_name]

