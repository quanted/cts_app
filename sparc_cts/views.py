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
        prop = request.POST.get("prop")
        structure = request.POST.get("chemical")

        postData = {
            "calc": calc,
            "prop": prop
        }

        calcObj = SPARC_Calc(structure)
        returnedData = calcObj.makeDataRequest() # make call for data!
        result = calcObj.getPropertyValue(prop)

        postData.update({"data": result}) # add that data

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