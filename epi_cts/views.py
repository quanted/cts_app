
from django.shortcuts import render
from django.http import HttpResponse

import logging
import os
import requests
import json
import redis

from epi_calculator import EpiCalc
from REST.smilesfilter import parseSmilesByCalculator


def request_manager(request):
	"""
	  less_simple_proxy takes a request and
	  makes the proper call to the TEST web services.
	  it relies on the epi_calculator to do such.

	  input: {"calc": [calculator], "prop": [property]}
	  output: returns data from TEST server
	  """

	EPI_URL = os.environ["CTS_EPI_SERVER"]

	calc = request.POST.get("calc")
	prop = request.POST.get("prop")
	structure = request.POST.get("chemical")
	sessionid = request.POST.get('sessionid')

	try:
		props = request.POST.getlist("props[]")  # expecting None if none
	except AttributeError:
		props = request.POST.get("props")

	postData = {
		'calc': calc,
		'props': props
	}

	try:
		# ++++++++++++++++++++++++ smiles filtering!!! ++++++++++++++++++++
		filtered_smiles = parseSmilesByCalculator(structure, "epi") # call smilesfilter

		logging.info("EPI receiving SMILES: {}".format(filtered_smiles))

		if '[' in filtered_smiles or ']' in filtered_smiles:
			logging.warning("EPI ignoring request due to brackets in SMILES..")
			postData.update({'error': "EPI Suite cannot process charged species or metals (e.g., [S+], [c+])"})
			return HttpResponse(json.dumps(postData), content_type='application/json')

		logging.info("EPI Filtered SMILES: {}".format(filtered_smiles))
		# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	except Exception as err:
		logging.warning("Error filtering SMILES: {}".format(err))
		postData.update({'error': "Cannot filter SMILES for TEST data"})
		return HttpResponse(json.dumps(postData), content_type='application/json')

	calcObj = EpiCalc()
	epi_results = []

	for prop in props:

		data_obj = {
			"calc": calc,
			"prop": prop
		}

		try:
			response = calcObj.makeDataRequest(filtered_smiles, calc, prop) # make call for data!
			data_obj.update({"data": json.loads(response.content)}) # add that data

			# node/redis stuff:
			if sessionid:
				result_json = json.dumps(data_obj)
				r = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)
				r.publish(sessionid, result_json)
			else:
				# if node ain't there, append to data list and send as HttpResponse:
				epi_results.append(data_obj)

		except Exception as err:
			logging.warning("Exception occurred getting TEST data: {}".format(err))
			data_obj.update({'error': "cannot reach TEST calculator"})

			logging.info("##### session id: {}".format(sessionid))

			# node/redis stuff:
			if sessionid: 
				r = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)
				r.publish(sessionid, json.dumps(data_obj))
			else:
				epi_results.append(data_obj)

	postData.update({'data': epi_results})

	return HttpResponse(json.dumps(postData), content_type='application/json')

	# except requests.HTTPError as e:
	# 	logging.warning("HTTP Error occurred: {}".format(e))
	# 	return HttpResponse(EPI_URL+e.msg, status=e.code, content_type='text/plain')

	# except ValueError as ve:
	# 	logging.warning("POST data is incorrect: {}".format(ve))
	# 	postData.update({"error": "value error"})
	# 	return HttpResponse(json.dumps(postData), content_type='application/json')