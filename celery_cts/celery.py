"""
CTS celery instance
"""
from __future__ import absolute_import
import os
from celery import Celery
import logging
import importlib
import json

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_apache')

# from django.conf import settings

# app = Celery('celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app = Celery(broker='redis://localhost:6379/0', 
				backend='redis://localhost:6379/0',
				include=['celery_cts.tasks'])

app.conf.update(
    CELERY_ACCEPT_CONTENT = ['json'],
	CELERY_TASK_SERIALIZER = 'json',
	CELERY_RESULT_SERIALIZER = 'json',
	# CELERYD_NODES=6,
	CELERY_NODES="test_worker chemaxon_worker epi_worker sparc_worker measured_worker manager_worker",
	CELERY_BIN="/var/www/ubertool/virtualenv/bin/celery",
	CELERY_APP="tasks:app",
	CELERYD_CHDIR="/var/www/ubertool/ubertool_cts",
	CELERYD_OPTS="-Q:1 test -c:1 1 \
		-Q:2 chemaxon -c:2 8 \
		-Q:3 epi -c:3 8 \
		-Q:4 sparc -c:4 1 \
		-Q:5 measured -c:5 1 \
		-Q:6 manager",
	CELERYD_USER="celery",
	CELERYD_GROUP="celery",
	CELERY_CREATE_DIRS=1,
	# %N will be replaced with the first part of the nodename.
	CELERYD_LOG_FILE="/var/log/celery/%N.log",
	CELERYD_PID_FILE="/var/run/celery/%N.pid",
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