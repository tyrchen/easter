# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.conf import settings

import json
import logging

TRUST_IPS = settings.TRUST_IPS or ['127.0.0.1']
logger  = logging.getLogger(__name__)

class Verification(object):
  """
  定义了一些验证方法。
  """
  def sorted_json(self, aim_item):
    if isinstance(aim_item, (basestring, int, long, float, bool)):
      return str(aim_item)
    elif isinstance(aim_item, (set, list, tuple)):
      return '&'.join([self.sorted_json(item) for item in aim_item])

    result = ''
    for key in sorted(aim_item.iterkeys()):
      result = result + '&' + json.dumps({key: self.sorted_json(aim_item[key])})
    return result

  def verify_info(self, sig, info):
    """
      验证请求的md5信息。
      TODO： 请求方式的改变，以字母排序，计算md5并验证。
    """
    import hashlib
    m = hashlib.md5()
    m.update(self.sorted_json(info))
    return sig == m.hexdigest()

  def verify_ip(self, ip):
    """
      验证请求的ip信息。
    """
    logger.info("Send ip %s " % ip)
    #print('ip is %s, trust_ip: %s, is trust: %s' % (ip, TRUST_IPS, ip in TRUST_IPS))
    return bool((ip in TRUST_IPS))