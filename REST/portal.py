"""
Routes calls from the browser to the proper 
webservices proxy (i.e., test-cts or jchem_rest).
"""

from django.http import HttpResponse, HttpRequest
import json
import logging
from celery_cts import tasks  # CTS tasks.py
import redis


redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


def directAllTraffic(request):

	sessionid = request.POST.get('sessionid')
	message = request.POST.get('message')  # list of json string data

	pchem_request = {}
	if message == "hello celery":
		# call test celery task:
		job = tasks.test_celery.delay(sessionid, message)
		return HttpResponse("hello celery test started")
	elif message:
		pchem_request = json.loads(message)
	else:
		pchem_request = json.loads(request.body)

	pchem_request['sessionid'] = sessionid  # add sessionid to request obj

	# check for cancel request:
	if 'cancel' in pchem_request.keys():
		tasks.removeUserJobsFromQueue.apply_async(args=[sessionid], queue="manager")  # use default IDs
		return HttpResponse(json.dumps({'status': "clearing user jobs from queues and redis"}), content_type='application/json')

	pchem_request_dict = pchem_request['pchem_request']
	user_jobs = []

	if 'nodes' in pchem_request.keys():
		# TODO: consider more efficient ways to parse up calls,
		for node in pchem_request['nodes']:
			pchem_request['node'] = node
			pchem_request['chemical'] = node['smiles']
			jobs = parseOutPchemCallsToWorkers(sessionid, pchem_request)
			user_jobs = user_jobs + jobs  # build single-level list of jobs

	else:
		user_jobs = parseOutPchemCallsToWorkers(sessionid, pchem_request)

	logging.info("caching jobs on redis")
	redis_conn.set(sessionid, json.dumps({'jobs': user_jobs}))

	return HttpResponse("Calculator tasks started!")


def parseOutPchemCallsToWorkers(sessionid, pchem_request):
	"""
	parses out calls to the celery workers by calculator.
	returning values are sent to user via redis messaging.
	returns user jobs list for caching
	"""

	pchem_request_dict = pchem_request['pchem_request']

	user_jobs = []

	if 'service' in pchem_request and pchem_request['service'] == 'getTransProducts':
		calc_request = HttpRequest()
		calc_request.POST = pchem_request
		try:
			job = tasks.startCalcTask.apply_async(args=["chemaxon", pchem_request], queue="chemaxon")
			user_jobs.append(job.id)
		except Exception as error:
			# logging.warning("error requesting {} props from {} calculator..\n {}".format(props, calc, error))
			error_response = {
				'calc': "chemaxon",
				'service': "getTransProducts",
				'error': "error requesting products from chemaxon"
			}
			redis_conn.publish(sessionid, json.dumps(error_response))

	elif 'service' in pchem_request and pchem_request['service'] == 'getSpeciationData':
		try:
			job = tasks.startCalcTask.apply_async(args=["chemaxon", pchem_request], queue="chemaxon")
			user_jobs.append(job.id)
		except Exception as error:
			error_response = {
				'calc': 'chemaxon',
				'service': "getSpeciationData",
				'error': "error requesting speciation data from chemaxon"
			}
			redis_conn.publish(sessionid, json.dumps(error_response))

	else:
		# loop calcs and run them as separate processes:
		for calc, props in pchem_request_dict.items():

			pchem_request.update({'calc': calc, 'props': props})

			calc_request = HttpRequest()
			calc_request.POST = pchem_request

			logging.info("requesting {} props from {} calculator..".format(props, calc))

			try:
				# NOTE: have to enable backend for celery to have linked callbacks for results
				job = tasks.startCalcTask.apply_async(args=[calc, pchem_request], queue=calc)  # use session for ID
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

	return user_jobs


def test_sockets(request):
	from django.template.loader import render_to_string
	
	html = render_to_string('cts_socket_test.html')
	return HttpResponse(html)