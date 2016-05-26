"""
CTS celery instance
"""
from __future__ import absolute_import
import os
from celery import Celery
import logging
import importlib
import json
from datetime import timedelta

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_apache')
from django.conf import settings

# app = Celery('celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app = Celery(broker='redis://localhost:6379/0', 
				backend='redis://localhost:6379/0',
				include=['celery_cts.tasks'])

app.conf.update(
    CELERY_ACCEPT_CONTENT = ['json'],
	CELERY_TASK_SERIALIZER = 'json',
	CELERY_RESULT_SERIALIZER = 'json',
	CELERYBEAT_SCHEDULE = {
		# executes daily at midnight:
		'clean-meta-leak-every-day': {
			'task': 'tasks.redis_garbage_collection',
			'schedule': crontab(minute=0, hour=0)
		}
		# executes every 5 seconds:
		'clean-meta-leak-test': {
			'task': 'tasks.redis_garbage_collection',
			'schedule': timedelta(seconds=5)
		}
	}
	# CELERYD_NODES=6,
	# CELERY_BIN="/var/www/ubertool/virtualenv/bin/celery",
	# CELERY_APP="tasks:app",
	# CELERYD_CHDIR="/var/www/ubertool/ubertool_cts",
	# CELERYD_USER="celery",
	# CELERYD_GROUP="celery",
	# CELERY_CREATE_DIRS=1,
	# %N will be replaced with the first part of the nodename.
	# CELERYD_LOG_FILE="/var/log/celery/%n.log",
	# CELERYD_PID_FILE="/var/run/celery/%n.pid",
	# CELERYD_LOG_FILE="%n.log",
	# CELERYD_PID_FILE="%n.pid",
)

# import celery_config  # import it first?
# app.config_from_object('celery_config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
