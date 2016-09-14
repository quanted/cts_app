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


def getCalcEndpoints(request):

	url = request.path

	if 'chemaxon' in url:
		calc = 'chemaxon'
	elif 'epi' in url:
		calc = 'epi'
	elif 'test' in url:
		calc = 'test'
	elif 'sparc' in url:
		calc = 'sparc'
	elif 'measured' in url:
		calc = 'measured'
	else: 
		return HttpResponse(json.dumps({'error': "calc not recognized"}), content_type='application/json')

	return cts_rest.CTS_REST().getCalcEndpoints(calc)


def getChemaxonInputs(request):
	"""
	ChemAxon input schema for running calculator
	"""
	chemaxon_obj = cts_rest.Chemaxon_CTS_REST()
	request_params = json.loads(request.body)
	chemaxon_request = HttpRequest()
	chemaxon_request.POST = request_params  # need rest of POST, not just chemical
	return chemaxon_obj.getChemaxonInputs(chemaxon_request)


def runChemaxon(request):
	chemaxon_obj = cts_rest.Chemaxon_CTS_REST()
	request_params = json.loads(request.body)
	chemaxon_request = HttpRequest()
	chemaxon_request.POST = request_params
	return chemaxon_obj.runChemaxon(chemaxon_request)


def getEpiInputs(request):
	"""
	EPI Suite input schema for running calculator
	"""
	epi_obj = cts_rest.EPI_CTS_REST()
	request_params = json.loads(request.body)
	epi_request = HttpRequest()
	epi_request.POST = request_params  # need rest of POST, not just chemical
	return epi_obj.getEpiInputs(epi_request)


def runEpi(request):
	"""
	EPI Suite input schema for running calculator
	"""
	epi_obj = cts_rest.EPI_CTS_REST()
	request_params = json.loads(request.body)
	epi_request = HttpRequest()
	epi_request.POST = request_params  # need rest of POST, not just chemical
	return epi_obj.runEpi(epi_request)


def getMeasuredInputs(request):
	"""
	EPI Suite input schema for running calculator
	"""
	epi_obj = cts_rest.Measured_CTS_REST()
	request_params = json.loads(request.body)
	epi_request = HttpRequest()
	epi_request.POST = request_params  # need rest of POST, not just chemical
	return epi_obj.getMeasuredInputs(epi_request)


def getSparcInputs(request):
	"""
	EPI Suite input schema for running calculator
	"""
	epi_obj = cts_rest.SPARC_CTS_REST()
	request_params = json.loads(request.body)
	sparc_request = HttpRequest()
	sparc_request.POST = request_params  # need rest of POST, not just chemical
	return epi_obj.getSparcInputs(sparc_request)

def getTestInputs(request):
	"""
	EPI Suite input schema for running calculator
	"""
	epi_obj = cts_rest.SPARC_CTS_REST()
	request_params = json.loads(request.body)
	test_request = HttpRequest()
	test_request.POST = request_params  # need rest of POST, not just chemical
	return epi_obj.getTestInputs(test_request)


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