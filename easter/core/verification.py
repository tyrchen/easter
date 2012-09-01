# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.conf import settings

TRUST_IPS = settings.TRUST_IPS or ['127.0.0.1', ]

class Verification(object):
  """
  定义了一些验证方法。
  """
  def verify_info(self, sig, info):
    """
      验证请求的md5信息。
    """
    return True #FUCKING !! Disable it
#    import md5
#    m = md5.new(info)
#    return sig == m.hexdigest()

  def verify_ip(self, ip):
    """
      验证请求的ip信息。
    """
    return bool((ip in TRUST_IPS))