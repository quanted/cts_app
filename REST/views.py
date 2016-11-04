"""
Calls CTS REST classes, functions linked to
CTS REST URLs - Swagger UI
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


def getCalcEndpoints(request, endpoint=None):

	cts_obj = cts_rest.CTS_REST()

	if not endpoint in cts_obj.endpoints:
		return HttpResponse(json.dumps({'error': "endpoint not recognized"}), content_type='application/json')		
	else:
		return cts_rest.CTS_REST().getCalcEndpoints(endpoint)


def getCalcInputs(request, calc=None):

	request_params = json.loads(request.body)

	prop, chemical = None, None

	if 'prop' in request_params:
		prop = request_params['prop']

	if 'chemical' in request_params:
		chemical = request_params['chemical']

	try:
		return cts_rest.CTS_REST().getCalcInputs(chemical, calc, prop)
	except Exception as e:
		return HttpResponse(json.dumps({'error': "{}".format(e)}), content_type='application/json')


def runCalc(request, calc=None):

	request_params = json.loads(request.body)
	calc_request = HttpRequest()
	calc_request.POST = request_params

	try:
		return cts_rest.CTS_REST().runCalc(calc, calc_request)
	except Exception as e:
		return HttpResponse(json.dumps({'error': "{}".format(e)}), content_type='application/json')



def runChemaxon(request):
	chemaxon_obj = cts_rest.Chemaxon_CTS_REST()
	request_params = json.loads(request.body)
	chemaxon_request = HttpRequest()
	chemaxon_request.POST = request_params
	return chemaxon_obj.runChemaxon(chemaxon_request)


def runEpi(request):
	"""
	EPI Suite input schema for running calculator
	"""
	epi_obj = cts_rest.EPI_CTS_REST()
	request_params = json.loads(request.body)
	epi_request = HttpRequest()
	epi_request.POST = request_params  # need rest of POST, not just chemical
	return epi_obj.runEpi(epi_request)


def runMeasured(request):
	"""
	EPI Suite input schema for running calculator
	"""
	measured_obj = cts_rest.Measured_CTS_REST()
	request_params = json.loads(request.body)
	measured_request = HttpRequest()
	measured_request.POST = request_params  # need rest of POST, not just chemical
	return measured_obj.runMeasured(measured_request)


def runSparc(request):
	"""
	EPI Suite input schema for running calculator
	"""
	sparc_obj = cts_rest.SPARC_CTS_REST()
	request_params = json.loads(request.body)
	sparc_request = HttpRequest()
	sparc_request.POST = request_params  # need rest of POST, not just chemical
	return sparc_obj.runSparc(sparc_request)


def testCTSNode(request):
	"""
	makes request to nodejs server 
	"""
	import requests
	from django.conf import settings

	response = requests.get(settings.NODEJS_URL + '/test')
	
	return HttpResponse(response.content)