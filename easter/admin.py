# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from django.contrib import admin
from easter.models import Event

class EventAdmin(admin.ModelAdmin):
  pass

admin.site.register(Event, EventAdmin)