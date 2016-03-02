__author__ = 'np'

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

import logging
import os
import requests
import json
import redis

from sparc_cts.views import request_manager as sparc_manager
from test_cts.views import request_manager as test_manager
from epi_cts.views import request_manager as epi_manager
from chemaxon_cts.views import request_manager as chemaxon_manager


# r = redis.StrictRedis(host='localhost', port=6379, db=0) # instantiate redis (where should this go???)
# logging.info("django redis client instantiated: {}".format(r))


# @csrf_exempt
def request_manager(request):

    try:

        logging.warning("incoming message to cts nodejs request manager: {}".format(request.POST))

        message = request.POST.get('message')
        sessionid = request.POST.get('sessionid') # session id created w/ client's socket id on node server

        logging.warning("for session id: {}".format(sessionid))

        if message == "new session":
            cache.set('sessionid', sessionid) # will this key collide with other users?!?!

        elif message == "close session":
            cache.delete(sessionid)

        return HttpResponse("cts received message from node")

    except Exception as e:
        logging.warning(e)
        # raise
        return HttpResponse("error occured in nodejs request manager")