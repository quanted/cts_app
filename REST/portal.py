"""
Routes calls from the browser to the proper 
webservices proxy (i.e., test-cts or jchem_rest).
"""

import requests
from django.http import HttpResponse
from chemaxon_cts import views as chemaxon_views
from epi_cts import views as epi_views
from sparc_cts import views as sparc_views
from test_cts import views as test_views
import logging
from smilesfilter import is_valid_smiles
import json


def directAllTraffic(request):
    webservice = request.POST.get('ws')

    # if webservice == 'getVersion':

    if webservice == 'validateSMILES':
        chemical = request.POST.get('chemical')
        json_results = json.dumps(is_valid_smiles(chemical)) # returns python dict
        return HttpResponse(json_results, content_type='application/json')
        # return HttpResponse(json.dumps({'isValid': isValid}), content_type='application/json')
    elif webservice == 'jchem':
        # note: jchem service is looking for 'service' and 'chemical'
        logging.info('directing to jchem..')
        return chemaxon_views.request_manager(request)
    elif webservice == 'epi':
        logging.info('directing to epi..')
        return epi_views.request_manager(request)
    elif webservice == 'sparc':
        logging.info('directing to sparc..')
        return sparc_views.request_manager(request)
    elif webservice == 'test':
        logging.info('directing to test..')
        return test_views.request_manager(request)
    else:
        return HttpResponse("error: service requested does not exist")