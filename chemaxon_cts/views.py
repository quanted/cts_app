from django.http import HttpResponse, HttpRequest
from django.core.cache import cache
import requests
import jchem_rest as jrest
import logging
import json
import redis
from jchem_calculator import JchemProperty as jp
from REST.smilesfilter import filterSMILES


# TODO: get these from the to-be-modified jchem_rest class..
services = ['getChemDetails', 'getChemSpecData', 'smilesToImage', 'convertToSMILES',
            'getTransProducts', 'getPchemProps', 'getPchemPropDict', 'getJchemVersion',
            'getMolecularInfo']


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
		service = request.POST.get('service')
		chemical = request.POST.get('chemical')
		prop = request.POST.get('prop')
		sessionid = request.POST.get('sessionid')  # None if it doesn't exist
		method = request.POST.get('method')
		ph = request.POST.get('ph')

		node = request.POST.get('node') # TODO: keep track of nodes without bringing node obj along for the ride!

		response = sendRequestToWebService(service, chemical, prop, ph, method, sessionid, node)  # returns json string

		return HttpResponse(response, content_type='application/json')

	except Exception as e:
		logging.warning("error occurred in request_manager: {}".format(e))
		raise HttpResponse(e)


def sendRequestToWebService(service, chemical, prop, phForLogD=None, method=None, sessionid=None, node=None):
	"""
    Makes call to jchem rest service
    """
	request = requests.Request(data={'chemical': chemical})
	if service == 'getChemDetails':
		# what about having this endpoint do the smiles conversion, filtering, then details...

		try:
			response = jrest.convertToSMILES(request)  # convert chemical to smiles
			response = json.loads(response.content)  # get json data

			# request.data = {'smiles': response['structure']}  # use converted smiles for next request
			# response = jrest.filterSMILES(request)  # filter smiles
			# response = json.loads(response.content)  # get json data

			filtered_smiles = filterSMILES(response['structure'])  # call CTS REST SMILES filter

			request.data = {'chemical': filtered_smiles}
			response = jrest.getChemDetails(request)  # get chemical details
			response = json.loads(response.content)

			# return this data in a standardized way for molecular info!!!!

		except Exception as e:
			raise e # TODO: build HTTP-code-specific error handling at portal.py
		


		response = jrest.getChemDetails(request).content
	elif service == 'getChemSpecData':
		response = jrest.getChemSpecData(request).content
	elif service == 'smilesToImage':
		response = jrest.smilesToImage(request).content
	elif service == 'convertToSMILES':
		response = jrest.convertToSMILES(request).content
	# elif service == 'getPchemProps':
	# 	response = getJchemPropData(chemical, prop, phForLogD, method, sessionid)
	elif service == 'getPchemPropDict':
		response = jrest.getpchemprops(request)  # gets pchemprop_model object..
	return response


def getJchemPropData(chemical, prop, phForLogD=None, method=None, sessionid=None, node=None):

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
	if method:
		resultDict['method'] = method

	result_json = json.dumps(resultDict)

	# node/redis stuff:
	if sessionid:
		r = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)
		r.publish(sessionid, result_json)

	return result_json