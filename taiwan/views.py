# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function

import logging
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)

class DisplayView(TemplateView):
  template_name = 'taiwan/display.html'
