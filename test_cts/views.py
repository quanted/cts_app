# from django.conf import settings # This urls.py file is looking for the TEST_CTS_PROXY_URL variable in the project settings.py file.
from django.shortcuts import render
from django.http import HttpResponse

import logging
import os
import requests
import json

from REST.calculator_map import TestCalc
from REST.calculator_map import EpiCalc
from REST.calculator_map import MeasuredCalc


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

  try:
    # get data from request
    calc = request.POST.get("calc")
    prop = request.POST.get("prop")

    # determine call url based on calc and prop:
    url = getUrlForCalcAndProp(calc, prop)
    async_request = requests.get(TEST_URL + url) # call TEST web services
    async_data = json.loads(async_request.content)

    returnedData = pickDataFromJson(calc, prop, async_data) # pick out data from molecule object
    postData = json.dumps({"calc": calc, "prop": prop, "data": returnedData})

  except requests.HTTPError as e:
    return HttpResponse(TEST_URL+e.msg, status=e.code, content_type='text/plain')

  except ValueError:
    return HttpResponse("Must send POST data to get response")

  else: 
    return HttpResponse(postData, content_type=async_request.headers['content-type'])


def getUrlForCalcAndProp(calc, prop):
  if calc == "test":
    Test = TestCalc() # make instance of TEST class
    return Test.getUrl("7", prop, "hierarchical")
  elif calc == "epi":
    Epi = EpiCalc()
    return Epi.getUrl("7", prop)
  elif calc == "measured":
    Measured = MeasuredCalc()
    return Measured.getUrl("7", prop)
  else:
    return ""


def pickDataFromJson(calc, prop, jsonData):
  Calc = getCalcObject(calc)
  try:
    key = Calc.propMap[prop]['resultKey']
    return jsonData[key]
  except AttributeError:
    logging.warning("Error occured picking data from json!")
    logging.warning("pickin key: {}, data: {}".format(key, jsonData))
    return "error: no calculator"
  except KeyError:
    logging.warning("Error occured picking data from json!")
    logging.warning("pickin key: {}, data: {}".format(key, jsonData))
    return "error"


def getCalcObject(calc):
  logging.info("Getting calc object for {}".format(calc))
  if calc == "test":
    return TestCalc()
  elif calc == "epi":
    return EpiCalc()
  elif calc == "measured":
    return MeasuredCalc()

