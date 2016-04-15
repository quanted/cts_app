"""
Monitors celery tasks on calculator queues
using flower
"""

import requests
import json
import redis
import logging
from django.http import HttpRequest

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


# class CTSFlower(object):

# 	def __init__(self):
# 		self.host = 'http://localhost'
# 		self.port = 5000
# 		self.baseUrl = self.host + ':' + str(self.port)
# 		self.queues = ['chemaxon', 'test', 'epi', 'sparc', 'measured']

# 	def getWorkers(self):
# 		response = requests.get(self.baseUrl + '/api/workers')
# 		return json.loads(response.content)

# 	def getTasks(self):
# 		response = requests.get(self.baseUrl + '/api/tasks')
# 		return json.loads(response.content)

# 	def getTasksByStatus(self, state):
# 		# e.g., /api/tasks?state=PENDING:
# 		url = self.baseUrl + '/api/tasks?taskname=tasks.startCalcTask&state=' + state
# 		response = requests.get(url)
# 		return json.loads(response.content)

# 	def abortRunningTask(self, task_id):
# 		url = self.baseUrl + '/api/task/abort/' + task_id
# 		# url = self.baseUrl + '/api/task/abort/'
# 		response = requests.post(url, headers={'Host': 'localhost:5000'})
# 		logging.info("abort response: {}".format(response))
# 		# return json.loads(response.content)
# 		return


def storeUserJobsToRedis(sessionid, user_jobs):
	"""
	expects list of celery job ids, stores them
	in redis using sessionid as key
	"""
	try:
		redis_conn.set(sessionid, json.dumps({'jobs':user_jobs}))
		logging.info("user {} data stored".format(sessionid))
	except Exception as e:
		raise e


def removeUserJobsFromRedis(sessionid):
	try:
		user_jobs_json = redis_conn.get(sessionid)  # all user's jobs

		logging.info("user's jobs: {}".format(user_jobs_json))
		
		if user_jobs_json:
			redis_conn.delete(sessionid)

		return True
		
	except Exception as e:
		raise e


# def getAllNonSuccessfulTasks():

# 	# TODO: turn into one call (e.g., ?state=PENDING&state=STARTED...)
#     pending_tasks = CTSFlower().getTasksByStatus("PENDING")
#     started_tasks = CTSFlower().getTasksByStatus("STARTED")
#     received_tasks = CTSFlower().getTasksByStatus("RECEIVED")

#     remaining_tasks = pending_tasks.keys() + started_tasks.keys() + received_tasks.keys()  # append lists

#     return remaining_tasks


def removeUserJobsFromQueue(sessionid, pchem_request_dict):
	"""
	call flower server to stop user's queued jobs.
	expects user_jobs as list
	"""
	from celery.task.control import revoke

	# without flower:
	user_jobs_json = redis_conn.get(sessionid)
	logging.info("JOBS: {}".format(user_jobs_json))

	if not user_jobs_json:
		logging.info("no user jobs, moving on..")
		return

	user_jobs = json.loads(user_jobs_json)
	for job_id in user_jobs['jobs']:
		# will this job object be recognized by celery instance "app"?
		revoke(job_id, terminate=True)  # stop user job
		logging.info("supposedly revoked {} task".format(job_id))

		redis_conn.publish(sessionid, json.dumps({'status': "p-chem data request canceled"}))

		# need to push something back to client to indicate its complete
		# for cts frontend case, that means removing the spinner (.html(""))

	# return HttpRequest("task canceled")


# def abortAllTasks():
# 	"""
# 	call flower server to stop user's queued jobs.
# 	expects user_jobs as list
# 	"""
# 	try:

# 		all_tasks = CTSFlower().getTasks()

# 		logging.info("aborting all tasks: {}".format(all_tasks))

# 		for task in all_tasks:
# 			logging.info("aborting job: {}".format(task))
# 			abort_response = CTSFlower().abortRunningTask(task)
# 			logging.info("task abort response: {}".format(abort_response))

# 		return "done!"

# 	except Exception as e:
# 		logging.info("problem: {}".format(e))
# 		raise e