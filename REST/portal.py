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


# test_queue_listener = tasks.startTESTQueueListener.delay()  # always listening for pchem request publishing


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

	# pchem_request['pchem_request'] is checkedCalcsAndProps,
	pchem_request_dict = pchem_request['pchem_request']

	# loop calcs and run them as separate processes:
	for calc, props in pchem_request_dict.items():

		logging.info("portal receiving web service: {}".format(calc))

		pchem_request.update({'calc': calc, 'props': props})

		# After parsing json string, wrap request with HttpRequest object for calc views:
		calc_request = HttpRequest()
		calc_request.POST = pchem_request

		if calc == 'validateSMILES':
			chemical = calc_request.POST.get('chemical')
			json_results = json.dumps(is_valid_smiles(chemical))  # returns python dict
			# return HttpResponse(json_results, content_type='application/json')
			# return HttpResponse(json.dumps({'isValid': isValid}), content_type='application/json')

		elif calc == 'chemaxon':
			logging.info('directing to jchem..')
			# job = tasks.startCalcTask.apply_async(args=[calc, pchem_request], queue="chemaxon")  # add job to TEST queue
			# return HttpResponse("Chemaxon job started!")
			chemaxon_views.request_manager(calc_request)

		# elif calc == 'epi':
		# 	logging.info('directing to epi..')
		# 	job = tasks.startEPITask.apply_async(args=[pchem_request], queue="EPI")  # add job to TEST queue
		# 	# return HttpResponse("SPARC job started!")
		# 	# return epi_views.request_manager(calc_request)

		# elif calc == 'sparc':
		# 	logging.info('directing to sparc..')
		# 	job = tasks.startSPARCTask.apply_async(args=[pchem_request], queue="SPARC")  # add job to TEST queue
		# 	# return HttpResponse("SPARC job started!")
		# 	# return sparc_views.request_manager(calc_request)

		elif calc == 'test':
			logging.info('directing to test..')
			job = tasks.startCalcTask.apply_async(args=[calc, pchem_request], queue="test")  # add job to TEST queue
			# logging.info("TEST job started: {}".format(job))
			# return HttpResponse("TEST job started!")

		# elif calc == 'measured':
		# 	logging.info('directing to measured..')
		# 	job = tasks.startMeasuredTask.apply_async(args=[pchem_request], queue="TEST")  # add job to TEST queue
		# 	# return measured_views.request_manager(calc_request)

		else:
			return HttpResponse("error: service requested does not exist")

	return HttpResponse("Calculator tasks started!")