"""
Routes calls from the browser to the proper 
webservices proxy (i.e., test-cts or jchem_rest).
"""

import requests
from django.http import HttpResponse
from chemaxon_cts import views as chemaxon_views
from epi_cts import views as epi_views
from sparc_cts import views as sparc_views
import logging
from smilesfilter import is_valid_smiles


def directAllTraffic(request):
    webservice = request.POST.get('ws')

    if webservice == 'validSMILES':
        return is_valid_smiles(request.POST.get('chemical'))
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
    else:
        return HttpResponse("error: service requested does not exist")