# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from pymongo import Connection
import sys

class Command(BaseCommand):
  args = "<app_name>"
  help = "Create a app to be stat"

  def handle(self, *args, **options):
    if len(args) != 1:
      print self.print_help(sys.argv[0], sys.argv[1])
      exit()
    app_name = args[0]
    confirm = raw_input('create a new app <%s>, Y/n?' % app_name)
    if not (confirm.startswith('Y') or confirm.startswith('y')):
      print 'aborted'
      exit()
    c = Connection()
    if app_name in c.database_names():
      print "\nDatabase %s already exists, please check." % app_name
      exit()
    app_token = "doN't_GuEss!"
    try:
      db = c[app_name]
      collection = db._meta
      collection.insert({'app_id': app_name, 'app_token': app_token})
    except Exception, e:
      print 'Error: %s' % str(e)
      exit()
    print "app <%s> has been created successfully."
    print "Please remember:"
    print "app_id=%s" % app_name
    print "app_token=%s" % app_token
