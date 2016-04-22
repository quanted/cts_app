"""
CTS celery instance
"""
from __future__ import absolute_import
import os
from celery import Celery
import logging
import importlib
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_apache')

from django.conf import settings

# app = Celery('celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app = Celery(broker='redis://localhost:6379/0', 
				backend='redis://localhost:6379/0',
				include=['celery_cts.tasks'])

# import celery_config  # import it first?
# app.config_from_object('celery_config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))