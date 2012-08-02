# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from djangorestframework.response import Response
from djangorestframework import status

import logging

logger = logging.getLogger(__name__)

err_codes = {
  0: 'ok',
  101: 'app does not exist',
  102: 'app token incorrect',
  200: 'invalid params',
  201: 'missing required param(s)',
  901: 'event quota exceeded',  #todo
}

class CodeResponse(Response):
  def __init__(self, code=0, status=status.HTTP_200_OK, headers=None, new_tid=None):
    self.new_tid = new_tid
    content = {'code': code, 'msg': err_codes.get(code, '')}
    super(CodeResponse, self).__init__(status, content, headers)
