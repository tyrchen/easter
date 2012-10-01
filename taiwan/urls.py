# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals, print_function

from django.conf.urls import patterns, url
from views import DisplayView

urlpatterns = patterns('',
    url(r'^$', view=DisplayView.as_view(), name='display'),
)
  