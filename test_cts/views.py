from django.http import HttpResponse

import logging
import os
import requests
import json
from test_calculator import TestCalc
from REST.smilesfilter import parseSmilesByCalculator

from celery import Celery
from django.conf import settings
import redis


redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


def request_manager(request):
	"""
	less_simple_proxy takes a request and
	makes the proper call to the TEST web services.
	it relies on the test_calculator to do such.

	input: {"calc": [calculator], "prop": [property]}
	output: returns data from TEST server
	"""

	TEST_URL = os.environ["CTS_TEST_SERVER"]
	postData = {}

	calc = request.POST.get("calc")
	# prop = request.POST.get("prop")

	try:
		props = request.POST.get("props[]")
		if not props:
			props = request.POST.getlist("props")
	except AttributeError:
		props = request.POST.get("props")

	calc_data = request.POST.get('checkedCalcsAndProps')
	structure = request.POST.get("chemical")
	sessionid = request.POST.get('sessionid')
	node = request.POST.get('node')

	if calc_data:
		calc = "test"
		props = calc_data['test']  # list of props

	postData = {
		"calc": calc,
		# "prop": prop
		# "props": props
	}

	# filter smiles before sending to TEST:
	# ++++++++++++++++++++++++ smiles filtering!!! ++++++++++++++++++++
	try:
		filtered_smiles = parseSmilesByCalculator(structure, calc) # call smilesfilter
	except Exception as err:
		logging.warning("Error filtering SMILES: {}".format(err))
		postData.update({'error': "Cannot filter SMILES for TEST data"})
		return HttpResponse(json.dumps(postData), content_type='application/json')
	# if '[' in filtered_smiles or ']' in filtered_smiles:
	#   logging.warning("TEST ignoring request due to brackets in SMILES..")
	#   postData.update({'error': "TEST cannot process charged species or metals (e.g., [S+], [c+])"})
	#   return HttpResponse(json.dumps(postData), content_type='application/json')
	logging.info("TEST Filtered SMILES: {}".format(filtered_smiles))
	# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	# test_results = tasked_calls.delay(sessionid, filtered_smiles, props)
	calcObj = TestCalc()
	test_results = []
	for prop in props:

		data_obj = {'calc': calc, 'prop':prop, 'node': node}

		try:
			logging.info("Calling TEST for {} data...".format(prop))

			response = calcObj.makeDataRequest(filtered_smiles, calc, prop)
			response_json = json.loads(response.content)

			logging.info("TEST response data for {}: {}".format(prop, response_json))

			# sometimes TEST data successfully returns but with an error:
			if response.status_code != 200:
				postData['data'] = "TEST could not process structure"
			else:
				test_data = response_json['properties'][calcObj.propMap[prop]['urlKey']]
				# data_obj['data'] = response_json['properties'][calcObj.propMap[prop]['urlKey']]
				if prop == 'water_sol':
					# data_obj['data'] = 1000 * 18.01528 * 10**test_data  # moles of h20, Log(mol/L) --> mg/L
					data_obj['data'] = 1000 * data_obj['data']['node']['mass'] * 10**test_data
				else:
					data_obj['data'] = test_data
				
			result_json = json.dumps(data_obj)

			# node/redis stuff:
			if redis_conn and sessionid:
				redis_conn.publish(sessionid, result_json)
			else:
				test_results.append(data_obj)

		except Exception as err:
			logging.warning("Exception occurred getting TEST data: {}".format(err))
			data_obj.update({'error': "data request timed out"})

			logging.info("##### session id: {}".format(sessionid))

			# node/redis stuff:
			if redis_conn and sessionid: 
				redis_conn.publish(sessionid, json.dumps(data_obj))
			else:
				test_results.append(data_obj)

	# TODO: Track this response when using celery, where does it go?
	postData.update({'data': test_results, 'props': props})
	return HttpResponse(json.dumps(postData), content_type='application/json')
	# return HttpResponse("retrieving TEST data..")