# from django.conf import settings # This urls.py file is looking for the TEST_CTS_PROXY_URL variable in the project settings.py file.
from django.shortcuts import render
from django.http import HttpResponse

import logging
import os
import requests
import json
from measured_calculator import MeasuredCalc
import redis
from REST.smilesfilter import parseSmilesByCalculator



def request_manager(request):

	calc = request.POST.get("calc")
	# props = request.POST.getlist("props[]")
	try:
		props = request.POST.getlist("props[]")  # expecting None if none
	except AttributeError:
		props = request.POST.get("props")

	structure = request.POST.get("chemical")
	sessionid = request.POST.get('sessionid')

	logging.info("Incoming data to Measured: {}, {}, {} (calc, props, chemical)".format(calc, props, structure))

	post_data = {
		"calc": calc,
		"props": props
	}

	logging.info("Measured receiving SMILES: {}".format(structure))

	try:
		filtered_smiles = parseSmilesByCalculator(structure, "epi") # call smilesfilter
	except Exception as err:
		logging.warning("Error filtering SMILES: {}".format(err))
		post_data.update({'error': "Cannot filter SMILES for Measured data"})
		return HttpResponse(json.dumps(post_data), content_type='application/json')

	logging.info("Measured Filtered SMILES: {}".format(filtered_smiles))

	calcObj = MeasuredCalc()
	measured_results = []

	try:
		response = calcObj.makeDataRequest(filtered_smiles) # make call for data!
		measured_data = json.loads(response.content)
		
		# get requested properties from results:
		for prop in props:
			data_obj = calcObj.getPropertyValue(prop, measured_data)

			# node/redis stuff:
			if sessionid:
				result_json = json.dumps(data_obj)
				r = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)
				r.publish(sessionid, result_json)
			else:
				# if node ain't there, append to data list and send as HttpResponse:
				measured_results.append(data_obj)

	except Exception as err:
		logging.warning("Exception occurred getting Measured data: {}".format(err))
		measured_results = []
		for prop in props:
			data_obj = {
				'error': "cannot find measured data for structure",
				'calc': "measured",
				'prop': prop
			}
			measured_results.append(data_obj)

		post_data.update({'data': measured_results})

		# node/redis stuff:
		if sessionid: 
			r = redis.StrictRedis(host='localhost', port=6379, db=0)  # instantiate redis (where should this go???)
			r.publish(sessionid, json.dumps(post_data))

		return HttpResponse(json.dumps(post_data), content_type='application/json')

	post_data.update({'data': measured_results})
	return HttpResponse(json.dumps(post_data), content_type='application/json')