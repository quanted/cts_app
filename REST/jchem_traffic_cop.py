from django.http import HttpResponse
import requests
import jchem_rest as jrest
import logging
import json
from jchem_rest import JchemProperty as jp


# TODO: get these from the to-be-modified jchem_rest class..
services = ['getChemDetails', 'getChemSpecData', 'smilesToImage', 'mrvToSmiles', 'getTransProducts', 'getPchemProps']


def directJchemTraffic(request):
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
		service = getRequestService(request)
		logging.info("service: {}".format(service))

		chemical = getRequestChemical(request)
		logging.info("chemical: {}".format(chemical))

		prop = getRequestProperty(request)
		logging.info("prop: {}".format(prop))

		if prop == 'kow_wph':
			ph = getRequestPh(request)
		else:
			ph = None

		response = sendRequestToWebService(service, chemical, prop, ph)
		return HttpResponse(response)

	except Exception as e:
		logging.warning("error occured in jchem_traffic_cop: {}".format(e))
		return HttpResponse(json.dumps({"error": "request error", "calc": "chemaxon", "prop": prop}))


def getRequestService(request):
	"""
	Picks out service name from request
	"""
	try:
		service = request.POST.get('service')
	except AttributeError as ae:
		logging.warning("attribute error -- {}".format(ae))
		raise
	except KeyError as ke:
		logging.warning("error: request as no key 'service' -- {}".format(ke))
		raise
	else:
		if service in services:
			return service
		else:
			raise KeyError("error: service {} is not recognized".format(service))


def getRequestChemical(request):
	"""
	Picks out chemical from request
	"""
	try:
		chemical = request.POST.get('chemical')
	except AttributeError as ae:
		logging.warning("error: request has no attribute 'POST' -- {}".format(ae))
		raise
	except KeyError as ke:
		logging.warning("error: request as no key 'chemical' -- {}".format(ke))
		raise
	else:
		return chemical


def getRequestProperty(request):
	"""
	Picks out property from request
	"""
	try:
		prop = request.POST.get('prop')
	except AttributeError as ae:
		logging.warning("error: request has no attribute 'POST' -- {}".format(ae))
		raise
	except KeyError as ke:
		logging.warning("error: request has no key 'prop' -- {}".format(ke))
		raise
	else:
		return prop


def getRequestPh(request):
	try:
		ph = request.POST.get('ph')
	except AttributeError as ae:
		logging.warning("error: request has no attribute 'POST' -- {}".format(ae))
		raise
	except KeyError as ke:
		logging.info("error: request has no key 'ph' -- {}".format(ke))
		pass
	else:
		return ph


def sendRequestToWebService(service, chemical, prop, phForLogD=None):
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
	elif service == 'mrvToSmiles':
		response = jrest.mrvToSmiles(request).content
	elif service == 'getPchemProps':
		response = getJchemPropData(chemical, prop, phForLogD)

	return response


def getJchemPropData(chemical, prop, phForLogD=None):
	result = ""

	if prop == 'water_sol':
		logging.info("water_sol prop")
		propObj = jp.getPropObject('solubility')
		propObj.makeDataRequest(chemical)
		result =  propObj.getSolubility()
		logging.info("water_sol result: {}".format(result))

	elif prop == 'ion_con':
		logging.info("'ion_con' prop")
		propObj = jp.getPropObject('pKa')
		propObj.makeDataRequest(chemical)
		result =  {'pKa': propObj.getMostAcidicPka(), 'pKb': propObj.getMostBasicPka()}
		logging.info("ion_con result: {}".format(result))

	elif prop == 'kow_no_ph':
		logging.info("'kow_no_ph' prop")
		propObj = jp.getPropObject('logP')
		propObj.makeDataRequest(chemical)
		result =  propObj.getLogP()
		logging.info("kow_no_ph result: {}".format(result))

	elif prop == 'kow_wph':
		logging.info("'kow_wph' prop")
		propObj = jp.getPropObject('logD')
		propObj.makeDataRequest(chemical)
		result =  propObj.getLogD(phForLogD)
		logging.info("kow_wph result: {}".format(result))

	else:
		result = None

	logging.info("Jchem prop result: {}".format(result))
	resultDict = json.dumps({"calc": "chemaxon", "prop":prop, "data":result})
	return resultDict