"""
CTS celery instance
"""
from __future__ import absolute_import
import os
from celery import Celery
import logging
# import importlib
# import json
# from datetime import timedelta
# from celery.schedules import crontab


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_apache')
from django.conf import settings


app = Celery(broker='redis://localhost:6379/0', 
				backend='redis://localhost:6379/0',
				include=['celery_cts.tasks'])

app.conf.update(
    CELERY_ACCEPT_CONTENT = ['json'],
	CELERY_TASK_SERIALIZER = 'json',
	CELERY_RESULT_SERIALIZER = 'json',
)

logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)