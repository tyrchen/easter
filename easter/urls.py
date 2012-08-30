# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from django.conf.urls import patterns, url
from views import EventView, UserEventsView

urlpatterns = patterns('',
    url(r'^v1/event/$', view=EventView.as_view(), name='event'),
    url(r'^v1/user/$', view=UserEventsView.as_view(), name='user_event'),
)
  