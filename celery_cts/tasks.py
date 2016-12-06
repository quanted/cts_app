from __future__ import absolute_import

import importlib
import logging
import os
import sys

from celery_cts._celery import app

path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    os.pardir))
# logging.info("adding path {} to sys for imports".format(path))
sys.path.append(path)


# @shared_task
# @app.task
# def startCalcTask(calc, request_post):

#     # TODO: try catch that works with celery task, for retries...

#     calc_views = importlib.import_module('.views', calc + '_cts')  # import calculator views

#     request = NotDjangoRequest()
#     request.POST = request_post

#     logging.info("Calling {} request_manager as celery task!".format(calc))

#     return calc_views.request_manager(request)


@app.task
def chemaxonTask(request_post):
    from cts_calcs.chemaxon_cts import worker
    request = NotDjangoRequest()
    request.POST = request_post
    logging.info("Request: {}".format(request_post))
    return worker.request_manager(request)


@app.task
def sparcTask(request_post):
    from cts_calcs.sparc_cts import worker
    request = NotDjangoRequest()
    request.POST = request_post
    return worker.request_manager(request)


@app.task
def epiTask(request_post):
    from cts_calcs.epi_cts import worker
    request = NotDjangoRequest()
    request.POST = request_post
    return worker.request_manager(request)


@app.task
def testTask(request_post):
    from cts_calcs.test_cts import worker
    request = NotDjangoRequest()
    request.POST = request_post
    return worker.request_manager(request)


@app.task
def measuredTask(request_post):
    from cts_calcs.measured_cts import worker
    request = NotDjangoRequest()
    request.POST = request_post
    return worker.request_manager(request)


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
    from . import cts_celery_manager

    logging.info("!!!received message: {}".format(message))
    cts_celery_manager.test_celery(sessionid, "hello from celery")
    # return HttpResponse("hello from celery!");


# temp patch for freeing celery from django while calc views
# are still relying on django.http Request...
class NotDjangoRequest(object):
    def __init__(self):
        self.POST = {}
