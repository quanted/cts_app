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

methods = ['KLOP', 'VG', 'PHYS']


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

	service = request.POST.get('service')
	chemical = request.POST.get('chemical')
	prop = request.POST.get('prop')
	sessionid = request.POST.get('sessionid')  # None if it doesn't exist
	method = request.POST.get('method')
	ph = request.POST.get('ph')
	node = request.POST.get('node') # TODO: keep track of nodes without bringing node obj along for the ride!
	calc = request.POST.get('calc')

	try:
		# props = request.POST.getlist("props[]")  # expecting None if none
		props = request.POST.get("props[]")
	except AttributeError:
		props = request.POST.get("props")

	postData = {
		'calc': calc,
		'props': props
	}

	if props:
		chemaxon_results = []
		for prop in props:

			data_obj = {'calc': calc, 'prop':prop}

			try:
				if prop == 'kow_wph' or prop == 'kow_no_ph':
					for method in methods:
						data_obj = sendRequestToWebService("getPchemProps", chemical, prop, ph, method, sessionid, node)  # returns json string
						chemaxon_results.append(data_obj)
				else:
					data_obj = sendRequestToWebService("getPchemProps", chemical, prop, ph, None, sessionid, node)  # returns json string
					chemaxon_results.append(data_obj)

				# node/redis stuff:
				if sessionid:
					result_json = json.dumps(data_obj)
					r = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)
					r.publish(sessionid, result_json)

			except Exception as err:
				logging.warning("Exception occurred getting chemaxon data: {}".format(err))
				data_obj.update({'error': "cannot reach chemaxon calculator"})

				logging.info("##### session id: {}".format(sessionid))

				# node/redis stuff:
				if sessionid: 
					r = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)
					r.publish(sessionid, json.dumps(data_obj))
				else:
					chemaxon_results.append(data_obj)

		postData.update({'data': chemaxon_results})  # list of data objects (keys: calc, prop, data)

		return HttpResponse(json.dumps(postData), content_type='application/json')


def sendRequestToWebService(service, chemical, prop, phForLogD=None, method=None, sessionid=None, node=None):
	"""
    Makes call to jchem rest service
    """
	request = requests.Request(data={'chemical': chemical})
	response = None
	if service == 'getChemDetails':
		try:
			response = jrest.convertToSMILES(request)  # convert chemical to smiles
			response = json.loads(response.content)  # get json data
			filtered_smiles = filterSMILES(response['structure'])  # call CTS REST SMILES filter
			request.data = {'chemical': filtered_smiles}
			response = jrest.getChemDetails(request)  # get chemical details
			response = json.loads(response.content)
		except Exception as e:
			raise e # TODO: build HTTP-code-specific error handling at portal.py
		response = jrest.getChemDetails(request).content
	elif service == 'getChemSpecData':
		response = jrest.getChemSpecData(request).content
	elif service == 'smilesToImage':
		response = jrest.smilesToImage(request).content
	elif service == 'convertToSMILES':
		response = jrest.convertToSMILES(request).content
	elif service == 'getPchemProps':
		response = getJchemPropData(chemical, prop, phForLogD, method, sessionid)
	return response


def getJchemPropData(chemical, prop, phForLogD=None, method=None, sessionid=None, node=None):
	"""
	Calls jchem web services from chemaxon and
	wraps data in a CTS data object (keys: calc, prop, method, data)
	"""

	resultDict = {"calc": "chemaxon", "prop": prop}

	result = ""
	if prop == 'water_sol':
		propObj = jp.getPropObject('solubility')
		propObj.makeDataRequest(chemical)
		result = propObj.getSolubility()
	elif prop == 'ion_con':
		propObj = jp.getPropObject('pKa')
		propObj.makeDataRequest(chemical)

		pkas = propObj.getMostAcidicPka() + propObj.getMostBasicPka()
		pkas.sort()

		result = {'pKa': pkas}
		# result = {'pKa': propObj.getMostAcidicPka(), 'pKb': propObj.getMostBasicPka()}
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

	return resultDict