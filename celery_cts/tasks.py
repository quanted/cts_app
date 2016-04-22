from __future__ import absolute_import
from celery import shared_task
from celery_cts.celery import app

import logging
import importlib
import json


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
	from REST import cts_celery_monitor

	logging.info("clearing celery task queues..")
	cts_celery_monitor.removeUserJobsFromQueue(sessionid)  # clear jobs from celery
	logging.info("clearing redis cache..")
	cts_celery_monitor.removeUserJobsFromRedis(sessionid)  # clear jobs from redis