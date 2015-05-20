# from django.conf import settings # This urls.py file is looking for the TEST_CTS_PROXY_URL variable in the project settings.py file.
from django.shortcuts import render
from django.http import HttpResponse

import logging
import os
import requests
import json

from calculator_map import Calculator as cmap

# simple_proxy is a method that reaches out to a predefined (in the settings.py file for the project) API server, in this case, hosting TEST endpoints
# It would expect a URL that would hit django that looks like http://yourdjangoserver/test_cts/api/TEST/SMILE/<endpoint>
# As of 10/22/14, TEST is responding to endpoints that include ALL, ALOGP, BP, KLOGP, MLOGP, MP, TEMPLATE, VP, WS, XLOGP, BP/MEASURED, MP/MEASURED, VP/MEASURED, and WS/MEASURED
# TODO: this function is strongly generic, it may be worth considering to use this as a component of the larger ubertool project for CTS/upstream. 
def simple_proxy(request, path):
  # TEST_URL = settings.TEST_CTS_PROXY_URL + path
  # TEST_URL = "http://127.0.0.1:8000/test_cts/api/" + path
  TEST_URL = os.environ["CTS_TEST_SERVER"] + path
  logging.info("Requested Url: {}".format(TEST_URL))

  try:
    async_request = requests.get(TEST_URL)
    async_data = async_request.content
  except requests.HTTPError as e:
    return HttpResponse(TEST_URL+e.msg, status=e.code, content_type='text/plain')
  else: 
    return HttpResponse(async_data, status=async_request.status_code, 
                        content_type=async_request.headers['content-type'])


def index(request,model):
  return render(request, 'test_cts/index')


def calc_kow(request):
  return render(request, 'calc_kow.html')


def less_simple_proxy(request):
  """
  less_simple_proxy takes a request and
  makes the proper call to the TEST web services.
  it relies on the calculator_map to do such.

  input: {"calc": [calculator], "prop": [property]}
  output: returns data from TEST server
  """

  TEST_URL = os.environ["CTS_TEST_SERVER"]
  postData = {}

  try:
    calc = request.POST.get("calc")
    prop = request.POST.get("prop")
    structure = request.POST.get("chemical")

    logging.info("{}".format(calc))
    logging.info("{}".format(prop))
    logging.info("{}".format(structure))

    postData = {
      "calc": calc,
      "prop": prop
    }

    # get data through calculator_map:
    calcObj = cmap.getCalcObject(calc) # get calculator object
    returnedData = calcObj.makeDataRequest(structure, calc, prop) # make call for data!
    # logging.info("DATA: {}".format(returnedData))

    postData.update({"data": returnedData}) # add that data

    logging.info("DATA: {}".format(postData))

    return HttpResponse(json.dumps(postData), content_type='application/json')

  except requests.HTTPError as e:
    logging.warning("HTTP Error occured: {}".format(e))
    return HttpResponse(TEST_URL+e.msg, status=e.code, content_type='text/plain')

  except ValueError as ve:
    logging.warning("POST data is incorrect: {}".format(ve))
    postData.update({"error": "value error"})
    return HttpResponse(json.dumps(postData), content_type='application/json')

  except requests.exceptions.ConnectionError as ce:
    logging.warning("Connection error occured: {}".format(ce))
    postData.update({"error": "connection error"})
    return HttpResponse(json.dumps(postData), content_type='application/json')