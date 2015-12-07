from django.http import HttpResponse
import requests
import jchem_rest as jrest
import logging
import json
from jchem_calculator import JchemProperty as jp


# TODO: get these from the to-be-modified jchem_rest class..
services = ['getChemDetails', 'getChemSpecData', 'smilesToImage', 'convertToSMILES',
				'getTransProducts', 'getPchemProps', 'getPchemPropDict']


def request_manager(request):
	"""
	Redirects request from frontend to the 
	approriate jchem web service. All calls going
	from browser to cts for jchem go through
	here first.

	Expects: data for requested service, and
	which name of service to call
	Format: {"service": "", "data": {usual POST data}}
	"""

	try:
		service = getRequestParam(request, 'service')
		chemical = getRequestParam(request, 'chemical')
		prop = getRequestParam(request, 'prop')

		if 'method' in request.POST: 
			method = getRequestParam(request, 'method')
		else:
			logging.info("no method specified..")
			method = None

		if prop == 'kow_wph':
			ph = getRequestParam(request, 'ph')
			logging.info("KOW PH: {}".format(ph))
		else:
			ph = None

		if service == 'getPchemPropDict':
			response = jrest.getpchemprops(request)
		else:
			response = sendRequestToWebService(service, chemical, prop, ph, method)

		logging.info("Jchem REPONSE: {}".format(response))

		return HttpResponse(response)

	except Exception as e:
		logging.warning("error occured in request_manager: {}".format(e))
		raise HttpResponse(e)


def getRequestParam(request, key):
	"""
	Picks out a key:value from request POST
	"""
	try:
		value = request.POST.get(key)
	except AttributeError as ae:
		logging.warning("attribute error -- {}".format(ae))
		raise
	except KeyError as ke:
		logging.warning("error: request has no key 'service' -- {}".format(ke))
		raise
	else:
		return value


# def getRequestPh(request):
# 	"""
# 	Picks out kow pH from request
# 	"""
# 	try:
# 		ph = request.POST.get('ph')
# 	except AttributeError as ae:
# 		logging.warning("error: request has no attribute 'POST' -- {}".format(ae))
# 		raise
# 	except KeyError as ke:
# 		logging.info("error: request has no key 'ph' -- {}".format(ke))
# 		pass
# 	else:
# 		return ph


def sendRequestToWebService(service, chemical, prop, phForLogD=None, method=None):
	"""
	Makes call to jchem rest service
	"""
	request = requests.Request(data={'chemical': chemical})
	if service == 'getChemDetails':
		response = jrest.getChemDetails(request).content
	elif service == 'getChemSpecData':
		response = jrest.getChemSpecData(request).content
	elif service == 'smilesToImage':
		response = jrest.smilesToImage(request).content
	elif service == 'convertToSMILES':
		response = jrest.convertToSMILES(request).content
	elif service == 'getPchemProps':
		response = getJchemPropData(chemical, prop, phForLogD, method)
	return response


def getJchemPropData(chemical, prop, phForLogD=None, method=None):

	logging.info("> prop: {}".format(prop))
	logging.info("> chemical: {}".format(chemical))
	logging.info("> method: {}".format(method))

	resultDict = {"calc": "chemaxon", "prop": prop}

	result = ""
	if prop == 'water_sol':
		propObj = jp.getPropObject('solubility')
		propObj.makeDataRequest(chemical)
		result = propObj.getSolubility()
	elif prop == 'ion_con':
		propObj = jp.getPropObject('pKa')
		propObj.makeDataRequest(chemical)
		result = {'pKa': propObj.getMostAcidicPka(), 'pKb': propObj.getMostBasicPka()}
	elif prop == 'kow_no_ph':
		propObj = jp.getPropObject('logP')
		propObj.makeDataRequest(chemical, method)
		result = propObj.getLogP()
	elif prop == 'kow_wph':
		propObj = jp.getPropObject('logD')
		propObj.makeDataRequest(chemical, method)
		result = propObj.getLogD(phForLogD)
	else:
		result = None

	# ADD METHOD KEY:VALUE IF LOGD OR LOGP...
	resultDict['data'] = result
	if method: resultDict['method'] = method

	result_json = json.dumps(resultDict)

	# resultDict = json.dumps({"calc": "chemaxon", "prop": prop, "data": result})
	return result_json