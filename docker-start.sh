#!/bin/bash

django-admin collectstatic --noinput         # "Collect" static files (--noinput executes the command w/o user interaction)
django-admin migrate auth --noinput          # used for login
django-admin migrate sessions --noinput      # used for login
exec uwsgi /etc/uwsgi/uwsgi.ini              # Start uWSGI (HTTP router that binds Python WSGI to a web server, e.g. NGINX)