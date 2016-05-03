from __future__ import absolute_import
from celery import shared_task
from celery_cts._celery import app

import logging
import importlib
import json
import sys, os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
    os.pardir))
logging.info("adding path {} to sys for imports".format(path))
sys.path.append(path)


# @shared_task
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


# @shared_task
@app.task
def removeUserJobsFromQueue(sessionid):
	"""
	call flower server to stop user's queued jobs.
	expects user_jobs as list
	"""
	# from REST import cts_celery_manager
	from . import cts_celery_manager

	logging.info("clearing celery task queues..")
	cts_celery_manager.removeUserJobsFromQueue(sessionid)  # clear jobs from celery
	logging.info("clearing redis cache..")
	cts_celery_manager.removeUserJobsFromRedis(sessionid)  # clear jobs from redis


@app.task
def test_celery(sessionid, message):
	from django.http import HttpResponse
	from . import cts_celery_manager

	logging.info("received message: {}".format(message))
	cts_celery_manager.test_celery(sessionid, "hello from celery")
	# return HttpResponse("hello from celery!");