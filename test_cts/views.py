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

# celery stuff:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_local')
app = Celery('cts_tasks', broker='redis://localhost:6379/0')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


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
		props = request.POST.get("props[]")  # expecting None if none
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
			response = calcObj.makeDataRequest(filtered_smiles, calc, prop)


			response_json = json.loads(response.content)
			logging.info("response data: ".format(response_json))

			# sometimes TEST data successfully returns but with an error:
			if response.status_code != 200:
				# data_obj['error'] = "TEST could not process structure"
				postData['data'] = "TEST could not process structure"
			else:
				data_obj['data'] = response_json['properties'][calcObj.propMap[prop]['urlKey']]
				
			result_json = json.dumps(data_obj)

			# node/redis stuff:
			if sessionid:
				r = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)
				r.publish(sessionid, result_json)
			else:
				test_results.append(data_obj)

		except requests.HTTPError as e:
			logging.info("HTTPError occurred getting TEST data: {}: {}".format(e.code, e.message))
			if e.code == 408:
				data_obj.update({'error': "data request timed out"})
			elif e.code == 500 or e.code == 404:
				data_obj.update({'error': "cannot reach TEST calculator"})
			else:
				data_obj.update({'error': e.message})
			# return HttpResponse(json.dumps(data_obj), content_type='application/json')
		except Exception as err:
			logging.warning("Exception occurred getting TEST data: {}".format(err))
			data_obj.update({'error': "cannot reach TEST calculator"})

			logging.info("##### session id: {}".format(sessionid))

			# node/redis stuff:
			if sessionid: 
				r = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)
				r.publish(sessionid, json.dumps(data_obj))
			else:
				test_results.append(data_obj)

	# TODO: Track this response when using celery, where does it go?
	postData.update({'data': test_results, 'props': props})
	return HttpResponse(json.dumps(postData), content_type='application/json')
	# return HttpResponse("retrieving TEST data..")