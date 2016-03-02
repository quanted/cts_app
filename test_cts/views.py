from django.http import HttpResponse

import logging
import os
import requests
import json
import redis

from test_calculator import TestCalc
from REST.smilesfilter import parseSmilesByCalculator


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
    # prop = request.POST.get("prop")
    props = request.POST.getlist("props[]")
    structure = request.POST.get("chemical")
    sessionid = request.POST.get('sessionid')

    postData = {
      "calc": calc,
      # "prop": prop
      "props": props
    }

    # filter smiles before sending to TEST:
    # ++++++++++++++++++++++++ smiles filtering!!! ++++++++++++++++++++
    filtered_smiles = parseSmilesByCalculator(structure, "test") # call smilesfilter
    # if '[' in filtered_smiles or ']' in filtered_smiles:
    #   logging.warning("TEST ignoring request due to brackets in SMILES..")
    #   postData.update({'error': "TEST cannot process charged species or metals (e.g., [S+], [c+])"})
    #   return HttpResponse(json.dumps(postData), content_type='application/json')
    logging.info("TEST Filtered SMILES: {}".format(filtered_smiles))
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    calcObj = TestCalc()

    test_results = []
    for prop in props:
        data_obj = {'calc':'test', 'prop':prop}
        response = calcObj.makeDataRequest(filtered_smiles, calc, prop)
        response_json = json.loads(response.content)
        data_obj['data'] = response_json
        test_results.append(data_obj)

        # node/redis stuff:
        if sessionid:
            result_json = json.dumps(data_obj)
            r = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)
            r.publish(sessionid, result_json)

    postData.update({'data': test_results})

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