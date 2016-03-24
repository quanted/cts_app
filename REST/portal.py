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
from nodejs_cts import views as nodejs_views
from smilesfilter import is_valid_smiles

import json
import logging
import redis
from celery import Celery
import tasks  # CTS tasks.py

import os


# @csrf_exempt
def directAllTraffic(request):

	sessionid = request.POST.get('sessionid')
	message = request.POST.get('message')  # list of json string data

	pchem_request = {}
	if message:
		pchem_request = json.loads(message)
	else:
		pchem_request = json.loads(request.body)

	# Expect following keys from parsed message: chemical, ph, calc, props, node

	pchem_request['sessionid'] = sessionid  # add sessionid to request obj

	# After parsing json string, wrap request with HttpRequest object for calc views:
	calc_request = HttpRequest()
	calc_request.POST = pchem_request



	# webservice = request.POST.get('calc')
	webservice = pchem_request['calc']  # TODO: see if smiles fiter gets called from here with Chemical Editor!!



	logging.info("portal receiving web service: {}".format(webservice))

	if webservice == 'validateSMILES':
		chemical = calc_request.POST.get('chemical')
		json_results = json.dumps(is_valid_smiles(chemical))  # returns python dict
		return HttpResponse(json_results, content_type='application/json')
		# return HttpResponse(json.dumps({'isValid': isValid}), content_type='application/json')

	elif webservice == 'chemaxon':
		logging.info('directing to jchem..')
		return chemaxon_views.request_manager(calc_request)

	elif webservice == 'epi':
		logging.info('directing to epi..')
		return epi_views.request_manager(calc_request)

	elif webservice == 'sparc':
		logging.info('directing to sparc..')
		return sparc_views.request_manager(calc_request)

	elif webservice == 'test':

		logging.info('directing to test..')

		if sessionid:
			# run TEST as subprocess if node server is up:
			job = tasks.startTESTTask.delay(calc_request)
			logging.info("TEST job started: {}".format(job))
			return HttpResponse("TEST job started")
		else:
			return test_views.request_manager(calc_request)

	elif webservice == 'measured':
		return measured_views.request_manager(calc_request)

	else:
		return HttpResponse("error: service requested does not exist")


# def parseRequestByCalculator(request):
# 	"""
# 	parses out request for p-chem data
# 	to each calculator views, which has its
# 	own queuing
# 	"""

# 	sessionid = request.POST.get('sessionid')
# 	message = request.POST.get('message')  # list of json string data

# 	pchem_request = {}
# 	if message:
# 		pchem_request = json.loads(message)
# 	else:
# 		pchem_request = json.loads(request.body)

# 	for calc, calc_data in pchem_request['pchem_data'].items():

# 		request_data = {
# 			'props': calc_data, 
# 			'sessionid': sessionid, 
# 			'calc': calc, 
# 			'chemical': pchem_request['chemical'],
# 			'ph': pchem_request['ph']
# 		}

# 		if calc == 'test':
# 			if sessionid:
# 				job = tasks.startTESTTask.delay(request_data)  # run TEST as sub process
# 				logging.info("TEST job started: {}".format(job))
# 			else:
# 				calc_request = HttpRequest()
# 				calc_request.POST = request_data
# 				calc_response = directAllTraffic(calc_request)	

# 		# chemaxon and sparc handle everything in views
# 		elif calc == 'chemaxon' or calc == 'sparc' or calc == 'epi':
# 			calc_request = HttpRequest()
# 			calc_request.POST = request_data
# 			calc_response = directAllTraffic(calc_request)

# 		# todo: refactor views 
# 		elif calc == 'epi':
# 			# loop each prop:
# 			for prop in calc_data:
# 				request_data.update({'prop': prop})
# 				calc_request = HttpRequest()  # TODO: wrap in directAllTraffic instead of here..
# 				calc_request.POST = request_data
# 				calc_response = directAllTraffic(calc_request)

# 	if sessionid:
# 		# TODO: use responses to track calls with celery
# 		# if sessionid, node is there and we're assuming data is publishing to redis
# 		# and getting to user via web socket/node
# 		return HttpResponse("things are ok")
# 	else:
# 		return calc_response