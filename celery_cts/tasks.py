import os
from celery import Celery
import logging
import importlib
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_apache')

from django.conf import settings

# app = Celery('celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app = Celery(broker='redis://localhost:6379/0')

import celery_config  # import it first?
# app.config_from_object('celery_config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)


@app.task
def startCalcTask(calc, request_post):
	from django.http import HttpRequest

	# TODO: try catch that works with celery task, for retries...

	calc_views = importlib.import_module('.views', calc + '_cts')  # import calculator views 

	# wrap post in django request:
	request = HttpRequest()
	request.POST = request_post

	logging.info("Calling {} request_manager as celery task!".format(calc))

	return calc_views.request_manager(request)


@app.task
def removeUserJobsFromQueue(sessionid):
	"""
	call flower server to stop user's queued jobs.
	expects user_jobs as list
	"""
	from REST import cts_celery_monitor

	logging.info("clearing celery task queues..")
	cts_celery_monitor.removeUserJobsFromQueue(sessionid)  # clear jobs from celery
	logging.info("clearing redis cache..")
	cts_celery_monitor.removeUserJobsFromRedis(sessionid)  # clear jobs from redis