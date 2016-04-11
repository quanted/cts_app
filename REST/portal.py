"""
Routes calls from the browser to the proper 
webservices proxy (i.e., test-cts or jchem_rest).
"""

import requests
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from chemaxon_cts import views as chemaxon_views
from epi_cts import views as epi_views
from sparc_cts import views as sparc_views
from test_cts import views as test_views
from measured_cts import views as measured_views
from smilesfilter import is_valid_smiles
import json
import logging
import tasks  # CTS tasks.py
import redis
import cts_celery_monitor


redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


# @csrf_exempt
def directAllTraffic(request):

	sessionid = request.POST.get('sessionid') 
	message = request.POST.get('message')  # list of json string data

	pchem_request = {}
	if message:
		pchem_request = json.loads(message)
	else:
		pchem_request = json.loads(request.body)

	pchem_request['sessionid'] = sessionid  # add sessionid to request obj


	# check for cancel request:
	if 'cancel' in pchem_request.keys():
		cts_celery_monitor.removeUserJobsFromQueue(sessionid)


	# pchem_request['pchem_request'] is checkedCalcsAndProps,
	pchem_request_dict = pchem_request['pchem_request']

	user_jobs = []

	# loop calcs and run them as separate processes:
	for calc, props in pchem_request_dict.items():

		pchem_request.update({'calc': calc, 'props': props})

		calc_request = HttpRequest()
		calc_request.POST = pchem_request

		logging.info("requesting {} props from {} calculator..".format(props, calc))

		try:
			job = tasks.startCalcTask.apply_async(args=[calc, pchem_request], queue=calc)  # put job on calc queue
			user_jobs.append(job.id)

		except Exception as error:
			logging.warning("error requesting {} props from {} calculator..\n {}".format(props, calc, error))
			if redis_conn and sessionid:
				error_response = {
					'calc': calc,
					'props': props,
					'error': "error requesting props for {}".format(calc)
				}
				redis_conn.publish(sessionid, json.dumps(error_response))
			else:
				return HttpResponse(json.dumps(error_response), content_type='application/json')

	# do this at views level:
	# cts_celery_monitor.storeUserJobsToRedis(sessionid, user_jobs)

	return HttpResponse("Calculator tasks started!")