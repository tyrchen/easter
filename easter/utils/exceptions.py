# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

class NotExistsException(Exception):
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return self.name.encode('utf-8')

class MongoDBHandleException(Exception):
  def __init__(self, handle):
    self.handle = handle

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return self.handle.encode('utf-8')

class NothingException(Exception):
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return self.name.encode('utf-8')

class SignitureException(Exception):
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return self.name.encode('utf-8')

class InfoIllegalException(Exception):
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return self.name.encode('utf-8')