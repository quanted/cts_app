#!/usr/bin/env python
import os
import django
from django.core.management import call_command

# initialize the app registry — django-admin/manage.py do this for you,
# but calling call_command() directly does not.
django.setup()

call_command("migrate", "auth", "--noinput")
call_command("migrate", "sessions", "--noinput")

# hand off to uwsgi, replacing this process (PID 1)
os.execvp("uwsgi", ["uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"])
