# from django.conf import settings # This urls.py file is looking for the TEST_CTS_PROXY_URL variable in the project settings.py file.
from django.shortcuts import render
from django.http import HttpResponse

import logging
import os
import requests
import json
from sparc_calculator import SPARC_Calc



def request_manager(request):
    # input: {"calc": [calculator], "prop": [property]}
    # output: returns data from TEST server


    try:
        calc = request.POST.get("calc")
        props = request.POST.get("props")
        structure = request.POST.get("chemical")

        postData = {
            "calc": calc,
            "props": props
        }

        calcObj = SPARC_Calc(structure)
        returnedData = calcObj.makeDataRequest() # make call for data!

        # sparc makes one big call and returns all data in one large json packet
        # that means either sparc's calculator should be able to pick them out,
        # or the front end should be able to loop multiple props at once.

        # "calculatorResults" value is list objects with same keys but different values:
        # {
        #   "type": "VAPOR_PRESSURE",
        #   "units": "logAtm",
        #   "pressure": 760,
        #   "temperature": 25,
        #   "meltingPoint": 0,
        #   "result": -0.86,
        #   "messageString": "vapor_pressure.\n0.\n25.0.\n",
        #   "batchString": "'0.'.\n''none'.'.\n'25.0.'.\n'0.0.'.\n'vp.'.\n"
        # },

        # result = calcObj.getPropertyValue(prop)

        postData.update({"calc": "sparc", "props": props, "data": returnedData}) # add that data

        #resultDict = json.dumps({"calc": "sparc", "prop": prop, "data": result})
        return HttpResponse(json.dumps(postData), content_type='application/json')


    except requests.HTTPError as e:
        logging.warning("HTTP Error occured: {}".format(e))
        return HttpResponse(e.msg, status=e.code, content_type='text/plain')

    except ValueError as ve:
        logging.warning("POST data is incorrect: {}".format(ve))
        postData.update({"error": "value error"})
        return HttpResponse(json.dumps(postData), content_type='application/json')

    except requests.exceptions.ConnectionError as ce:
        logging.warning("Connection error occured: {}".format(ce))
        postData.update({"error": "connection error"})
        return HttpResponse(json.dumps(postData), content_type='application/json')