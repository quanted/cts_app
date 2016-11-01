#!/bin/bash

django-admin.py collectstatic --noinput       # "Collect" static files (-l = use symbolic links instead of copying files)
exec uwsgi /etc/uwsgi/uwsgi.ini               # Start uWSGI