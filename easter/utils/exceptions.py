# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

import traceback
import logging

logger = logging.getLogger(__name__)

class PrintTraceBackException(Exception):
  def __init__(self, name):
    super(PrintTraceBackException, self).__init__()
    self.name = name
    logger.info("%s:\n%s" %(self.name, traceback.format_exc()))

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return self.name.encode('utf-8')

class NotExistsException(PrintTraceBackException):
  pass

class MongoDBHandleException(PrintTraceBackException):
  pass

class NothingException(PrintTraceBackException):
  pass

class SignitureException(PrintTraceBackException):
  pass

class InfoIllegalException(PrintTraceBackException):
  pass