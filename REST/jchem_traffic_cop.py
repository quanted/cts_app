from django.http import HttpResponse
import requests
import jchem_rest as jrest
import logging
import json


# TODO: get these from the to-be-modified jchem_rest class..
services = ['getChemDetails', 'getChemSpecData', 'smilesToImage', 'mrvToSmiles', 'getTransProducts']


def directTraffic(request):
	"""
	Redirects request from frontend to the 
	approriate jchem web service. All calls going
	from browser to cts for jchem go through
	here first.

	Expects: data for requested service, and
	which name of service to call
	Format: {"service": "", "data": {usual POST data}}
	"""

	# TODO: try except here (top level)
	try:
		requestService = getRequestService(request)
		requestChem = getRequestChemical(request)
		response = sendRequestToWebService(requestService, requestChem)
		return HttpResponse(response.content)
	except:
		return HttpResponse("error")


def getRequestService(request):
	"""
	Picks out service name from request
	"""
	service = ""
	try:
		service = request.POST.get('service')
	except AttributeError:
		logging.warning("attribute error")
		raise
	except KeyError:
		logging.warning("error: request as no key 'service'")
		raise
	else:
		if service in services:
			return service
		else:
			raise KeyError("error: service {} is not recognized".format(service))


def getRequestChemical(request):
	"""
	Picks out data from request
	"""
	chemical = ""
	try:
		chemical = request.POST.get('chemical')
	except AttributeError:
		logging.warning("error: request has no attribute 'POST'")
		raise
	except KeyError:
		logging.warning("error: request as no key 'chemical'")
		raise
	else:
		return chemical


def sendRequestToWebService(service, chemical):
	"""
	Makes call to jchem rest service
	"""
	request = requests.Request(data={'chemical': chemical})

	if service == 'getChemDetails':
		response = jrest.getChemDetails(request)
	elif service == 'getChemSpecData':
		response = jrest.getChemSpecData(request)
	elif service == 'smilesToImage':
		response = jrest.smilesToImage(request)
	elif service == 'mrvToSmiles':
		response = jrest.mrvToSmiles(request)

	return response