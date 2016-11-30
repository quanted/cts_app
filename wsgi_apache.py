"""
WSGI config for UberDjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os, sys

# Add Django project & parent directory to Python PATH
sys.path.insert(0, '/var/www/ubertool/ubertool_cts')
sys.path.insert(0, '/var/www/ubertool')
# Settings.py declaration
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ubertool_cts.settings_apache")

# Django project entry point (Apache/mod_wsgi & app.yaml)
# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()
# changed nov. 30 2016
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
