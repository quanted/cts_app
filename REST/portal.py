"""
Routes calls from the browser to the proper 
webservices proxy (i.e., test-cts or jchem_rest).
"""

from django.http import HttpResponse, HttpRequest
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

	# pchem_request['pchem_request'] is checkedCalcsAndProps,
	pchem_request_dict = pchem_request['pchem_request']

	# check for cancel request:
	if 'cancel' in pchem_request.keys():
		# default queue:
		tasks.removeUserJobsFromQueue.apply_async(args=[sessionid, pchem_request_dict], queue="manager")
		# tasks.removeUserJobsFromRedis.apply_async(args=[sessionid], queue="manager")
		# return "success" or "failure" response
		return HttpResponse(json.dumps({'status': "clearing user jobs from queues and redis"}), content_type='application/json')

	user_jobs = []

	# loop calcs and run them as separate processes:
	for calc, props in pchem_request_dict.items():

		pchem_request.update({'calc': calc, 'props': props})

		calc_request = HttpRequest()
		calc_request.POST = pchem_request

		logging.info("requesting {} props from {} calculator..".format(props, calc))

		try:
			# put job on calc queue:
			# job = tasks.startCalcTask.apply_async(args=[calc, pchem_request], queue=calc, link=tasks.cleanQueues.s(sessionid))
			job = tasks.startCalcTask.apply_async(args=[calc, pchem_request], queue=calc)
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
	logging.info("caching jobs on redis")
	redis_conn.set(sessionid, json.dumps({'jobs': user_jobs}))

	return HttpResponse("Calculator tasks started!")