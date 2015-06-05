# from django.conf import settings # This urls.py file is looking for the TEST_CTS_PROXY_URL variable in the project settings.py file.
from django.shortcuts import render
from django.http import HttpResponse

import logging
import os
import requests
import json
from epi_calculator import EpiCalc



def request_manager(request):
  """
  less_simple_proxy takes a request and
  makes the proper call to the TEST web services.
  it relies on the epi_calculator to do such.

  input: {"calc": [calculator], "prop": [property]}
  output: returns data from TEST server
  """

  EPI_URL = os.environ["CTS_EPI_SERVER"]
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

    # get data through epi_calculator:
    # calcObj = cmap.getCalcObject(calc) # get calculator object
    calcObj = EpiCalc()
    returnedData = calcObj.makeDataRequest(structure, calc, prop) # make call for data!
    # logging.info("DATA: {}".format(returnedData))

    postData.update({"data": returnedData}) # add that data

    logging.info("DATA: {}".format(postData))

    return HttpResponse(json.dumps(postData), content_type='application/json')

  except requests.HTTPError as e:
    logging.warning("HTTP Error occured: {}".format(e))
    return HttpResponse(EPI_URL+e.msg, status=e.code, content_type='text/plain')

  except ValueError as ve:
    logging.warning("POST data is incorrect: {}".format(ve))
    postData.update({"error": "value error"})
    return HttpResponse(json.dumps(postData), content_type='application/json')

  except requests.exceptions.ConnectionError as ce:
    logging.warning("Connection error occured: {}".format(ce))
    postData.update({"error": "connection error"})
    return HttpResponse(json.dumps(postData), content_type='application/json')