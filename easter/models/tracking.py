# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'tchen'

from pymongo import Connection

import logging
logger = logging.getLogger(__name__)

connection = Connection()

class Tracker(object):
  db_model = 'tracking'

  @classmethod
  def get_by_id(cls, id):
    return
