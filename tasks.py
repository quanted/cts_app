from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
import logging
import redis
import importlib
import json


redis_conn = redis.StrictRedis(host='localhost', port='6379', db=0)


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_apache')
# settings.configure()

app = Celery('cts_celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

# app.conf.CELERY_ALWAYS_EAGER = True  # NOTE: This might be forcing workers to run synchronously
# app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

from celery.utils import LOG_LEVELS
app.conf.CELERYD_LOG_LEVEL = LOG_LEVELS['DEBUG']
app.conf.CELERY_RESULT_BACKEND = 'redis://'
app.conf.BROKER_URL = 'redis://localhost:6379/0'
app.conf.CELERY_ACCEPT_CONTENT = ['json']
app.conf.CELERY_TASK_SERIALIZER = 'json'
app.conf.CELERY_RESULT_SERIALIZER = 'json'


@app.task(max_retries=3)
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


@app.task
def finishedJob():
	"""
	callback for getting p-chem data
	from calculators. removes user jobs and
	user from celery and redis cache once
	data has returned
	"""
	logging.info("inside finished job subtask!")
	logging.info("what inputs are here???")
	# logging.info("is there an id? {}".format(uuid))
	logging.info("returning now..")
	return


# @app.task
# def removeUserJobsFromRedis(sessionid):
# 	"""
# 	call flower server to stop user's queued jobs.
# 	expects user_jobs as list
# 	"""
# 	from REST import cts_celery_monitor

# 	logging.info("inside clear redis task!!!")
# 	cts_celery_monitor.removeUserJobsFromRedis(sessionid)

# 	# return
