"""
Calls CTS REST classes, functions linked to
CTS REST URLs
"""

import cts_rest
from django.http import HttpRequest, HttpResponse
import json



def getSwaggerJsonContent(request):
	"""
	Opens up swagger.json content
	"""
	swag = open('static/swagger.json', 'r').read()
	swag_filtered = swag.replace('\n', '').strip()
	swag_obj = json.loads(swag_filtered)
	response = HttpResponse()
	response.write(json.dumps(swag_obj))
	return response


def getCTSEndpoints(request):
	"""
	CTS REST calculator endpoints
	"""
	cts_obj = cts_rest.CTS_REST()
	return cts_obj.getCTSREST()


def getChemaxonEndpoints(request):
	"""
	ChemAxon endpoints
	"""
	chemaxon_obj = cts_rest.Chemaxon_CTS_REST()
	return chemaxon_obj.getChemaxonREST()


def getChemaxonInputs(request):
	"""
	ChemAxon input schema for running calculator
	"""
	chemaxon_obj = cts_rest.Chemaxon_CTS_REST()
	request_params = json.loads(request.body)
	chemaxon_request = HttpRequest()
	chemaxon_request.POST = {'chemical': request_params['chemical']}  # need rest of POST, not just chemical
	return chemaxon_obj.getChemaxonInputs(chemaxon_request)