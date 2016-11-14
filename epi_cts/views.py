import logging
import os
import requests
import json
import redis

from epi_calculator import EpiCalc
from REST.smilesfilter import parseSmilesByCalculator


redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


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
	node = request.POST.get('node')
	run_type = request.POST.get('run_type')

	try:
		props = request.POST.get("props[]")
		if not props:
			props = request.POST.getlist("props")
	except AttributeError:
		props = request.POST.get("props")

	postData = {
		'calc': calc,
		# 'props': props
	}

	filtered_smiles = ''

	try:
		# ++++++++++++++++++++++++ smiles filtering!!! ++++++++++++++++++++
		filtered_smiles = parseSmilesByCalculator(structure, "epi") # call smilesfilter

		logging.info("EPI receiving SMILES: {}".format(filtered_smiles))

		if '[' in filtered_smiles or ']' in filtered_smiles:
			logging.warning("EPI ignoring request due to brackets in SMILES..")
			postData.update({'data': "EPI Suite cannot process charged species or metals (e.g., [S+], [c+])"})
			if redis_conn and sessionid:
				for prop in props:
					postData['prop'] = prop
					postData['node'] = node
					if run_type:
						postData['run_type'] = run_type
					redis_conn.publish(sessionid, json.dumps(postData))
				return

		logging.info("EPI Filtered SMILES: {}".format(filtered_smiles))
		# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	except Exception as err:
		logging.warning("Error filtering SMILES: {}".format(err))
		postData.update({'data': "Cannot filter SMILES for EPI data"})
		redis_conn.publish(sessionid, json.dumps(postData))

	calcObj = EpiCalc()
	epi_results = []

	if run_type == 'rest':
		props = [prop]  # rest api currently does single prop calls

	for prop in props:

		data_obj = {
			"calc": "epi",
			"prop": prop,
			'node': node,
			'request_post': request.POST
		}

		if run_type:
			data_obj['run_type'] = run_type

		try:
			response = calcObj.makeDataRequest(filtered_smiles, calc, prop) # make call for data!
			result_obj = json.loads(response.content)

			if 'propertyvalue' in result_obj:
				data_obj.update({'data': result_obj['propertyvalue']})
			else:
				data_obj.update({"data": json.loads(response.content)}) # add that data

			result_json = json.dumps(data_obj)
			redis_conn.publish(sessionid, result_json)

		except Exception as err:
			logging.warning("Exception occurred getting {} data: {}".format(err, calc))
			data_obj.update({'data': "cannot reach {} calculator".format(calc)})

			logging.info("##### session id: {}".format(sessionid))

			# node/redis stuff:
			redis_conn.publish(sessionid, json.dumps(data_obj))