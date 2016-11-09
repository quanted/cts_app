from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
# from .celery import app as celery_app  # noqa
from ._celery import app as celery_app
import os

try:
	from settings_local import *
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
except ImportError as e:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_apache')
	pass