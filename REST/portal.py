"""
Routes calls from the browser to the proper 
webservices proxy (i.e., test-cts or jchem_rest).
"""

import requests
from django.http import HttpResponse
from chemaxon_cts import views as chemaxon_views
from epi_cts import views as epi_views
import logging


def directAllTraffic(request):
    webservice = request.POST.get('ws')
    if webservice == 'jchem':
        # note: jchem service is looking for 'service' and 'chemical'
        logging.info('directing to jchem..')
        return chemaxon_views.request_manager(request)
    elif webservice == 'epi':
        logging.info('directing to test..')
        return epi_views.request_manager(request)
    elif webservice == 'sparc':
        pass
    else:
        return HttpResponse("error: service requested does not exist")