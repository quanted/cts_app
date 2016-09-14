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


redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


def request_manager(request):

	calc = request.POST.get("calc")
	# props = request.POST.getlist("props[]")
	try:
		props = request.POST.get("props[]")
		if not props:
			props = request.POST.getlist("props")
	except AttributeError:
		props = request.POST.get("props")

	structure = request.POST.get("chemical")
	sessionid = request.POST.get('sessionid')
	node = request.POST.get('node')
	run_type = request.POST.get('run_type')
	prop = request.POST.get('prop')

	logging.info("Incoming data to Measured: {}, {}, {} (calc, props, chemical)".format(calc, props, structure))

	post_data = {
		"calc": calc,
		"props": props,
	    'node': node
	}

	logging.info("Measured receiving SMILES: {}".format(structure))

	try:
		filtered_smiles = parseSmilesByCalculator(structure, "epi") # call smilesfilter
		if '[' in filtered_smiles or ']' in filtered_smiles:
			logging.warning("EPI ignoring request due to brackets in SMILES..")
			post_data.update({'error': "EPI Suite cannot process charged species or metals (e.g., [S+], [c+])"})
			return HttpResponse(json.dumps(post_data), content_type='application/json')
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

		if run_type == 'rest':
			props = [prop]
		
		# get requested properties from results:
		for prop in props:
			data_obj = calcObj.getPropertyValue(prop, measured_data)
			data_obj.update({'node': node})

			# push one result at a time if node/redis:
			if redis_conn and sessionid:
				result_json = json.dumps(data_obj)
				redis_conn.publish(sessionid, result_json)
			else:
				# otherwise send as list
				measured_results.append(data_obj)

	except Exception as err:
		logging.warning("Exception occurred getting Measured data: {}".format(err))
		measured_results = []
		for prop in props:
			data_obj = {
				'data': "error - cannot find measured data for structure",
				'calc': "measured",
				'prop': prop,
				'node': node
			}
			measured_results.append(data_obj)
			if redis_conn and sessionid:
				redis_conn.publish(sessionid, json.dumps(data_obj))

		if not sessionid:
			post_data.update({'data': measured_results, 'chemical': filtered_smiles})

		# if redis_conn and sessionid: 
		# 	redis_conn.publish(sessionid, json.dumps(post_data))
		# else:
			HttpResponse(json.dumps(post_data), content_type='application/json')

	if not sessionid:
		post_data.update({'data': measured_results, 'chemical': filtered_smiles})
		return HttpResponse(json.dumps(post_data), content_type='application/json')