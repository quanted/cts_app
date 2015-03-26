"""
Routes calls from the browser to the proper 
webservices proxy (i.e., test-cts or jchem_rest).
"""

import requests
from django.http import HttpResponse
import jchem_traffic_cop
from test_cts import views


def directAllTraffic(request):
	webservice = request.POST.get('ws')
	if webservice == 'jchem':
		# note: jchem service is looking for 'service' and 'chemical'
		return jchem_traffic_cop.directJchemTraffic(request)
	elif webservice == 'test':
		return views.less_simple_proxy(request)
	else:
		return HttpResponse("error: service requested does not exist")