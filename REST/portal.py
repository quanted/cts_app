"""
Routes calls from the browser to the proper 
webservices proxy (i.e., test-cts or jchem_rest).
"""

import requests
from django.http import HttpResponse
import jchem_traffic_cop
from epi_cts import views
import logging


def directAllTraffic(request):
    webservice = request.POST.get('ws')
    if webservice == 'jchem':
        # note: jchem service is looking for 'service' and 'chemical'
        logging.info('directing to jchem..')
        return jchem_traffic_cop.directJchemTraffic(request)
    elif webservice == 'test':
        logging.info('directing to test..')
        return views.less_simple_proxy(request)
    elif webservice == 'sparc':
        pass
    else:
        return HttpResponse("error: service requested does not exist")