#!/usr/bin/env python
import logging
import os
import django
from django.core.management import call_command

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("entrypoint")

django.setup()

# log.info("entrypoint: running collectstatic")
# call_command("collectstatic", "--noinput", "--clear")

log.info("entrypoint: running migrations")
call_command("migrate", "auth", "--noinput")
call_command("migrate", "sessions", "--noinput")

log.info("entrypoint: handing off to uwsgi")
os.execvp("uwsgi", ["uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"])