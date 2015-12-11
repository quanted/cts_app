# from django.conf import settings # This urls.py file is looking for the TEST_CTS_PROXY_URL variable in the project settings.py file.
from django.shortcuts import render
from django.http import HttpResponse

import logging
import os
import requests
import json
from test_calculator import TestCalc



def request_manager(request):
  """
  less_simple_proxy takes a request and
  makes the proper call to the TEST web services.
  it relies on the test_calculator to do such.

  input: {"calc": [calculator], "prop": [property]}
  output: returns data from TEST server
  """

  TEST_URL = os.environ["CTS_TEST_SERVER"]
  postData = {}

  try:
    calc = request.POST.get("calc")
    prop = request.POST.get("prop")
    structure = request.POST.get("chemical")

    postData = {
      "calc": calc,
      "prop": prop
    }


    calcObj = TestCalc()
    response = calcObj.makeDataRequest(structure, calc, prop) # make call for data!

    prop_data = json.loads(response.content)['properties'] # TEST props (MP, BP, etc.)
    logging.info(">>> {}".format(prop_data))
    prop_data = prop_data[calcObj.propMap[prop]['urlKey']]
    logging.info(">>> {}".format(prop_data))

    postData.update({"data": prop_data}) # add that data

    logging.info("TEST DATA: {}".format(postData))

    return HttpResponse(json.dumps(postData), content_type='application/json')

  except requests.HTTPError as e:
    logging.warning("HTTP Error occurred: {}".format(e))
    return HttpResponse(TEST_URL+e.msg, status=e.code, content_type='text/plain')

  except ValueError as ve:
    logging.warning("POST data is incorrect: {}".format(ve))
    postData.update({"error": "value error"})
    return HttpResponse(json.dumps(postData), content_type='application/json')

  except requests.exceptions.ConnectionError as ce:
    logging.warning("Connection error occurred: {}".format(ce))
    postData.update({"error": "connection error"})
    return HttpResponse(json.dumps(postData), content_type='application/json')