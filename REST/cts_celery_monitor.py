"""
Monitors celery tasks on calculator queues
using flower
"""

import requests
import json
import redis

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


class CTSFlower(object):

	def __init__(self):
		self.host = 'http://localhost'
		self.port = 5000
		self.baseUrl = self.host + ':' + str(self.port)
		self.queues = ['chemaxon', 'test', 'epi', 'sparc', 'measured']

	def getWorkers(self):
		response = requests.get(self.baseUrl + '/api/workers')
		return json.loads(response.content)

	def getTasks(self):
		response = requests.get(self.baseUrl + '/api/tasks')
		return json.loads(response.content)

	def getTasksByStatus(self, state):
		url = self.baseUrl + '/api/tasks?state=' + state  # e.g., /api/tasks?state=PENDING
		response = requests.get(url)
		return json.loads(response.content)

	def abortRunningTask(self, task_id):
		url = self.baseUrl + '/api/task/abort/' + task_id
		response = requests.get(url)
		return json.loads(response.content)


def storeUserJobsToRedis(sessionid, user_jobs):
	"""
	expects list of celery job ids, stores them
	in redis using sessionid as key
	"""
	try:
		redis_conn.set(sessionid, json.dumps(user_jobs))
	except Exception as e:
		raise e

def removeUserJobsFromQueue(sessionid, user_jobs):
	"""
	remove celery jobs from user's cache on redis,
	and call flower server to stop user's queued jobs.
	expects user_jobs as list
	"""
	try:

		# remove user's jobs from queues:
		pending_tasks = CTSFlower().getTasksByStatus("PENDING")
		for user_job in pending_tasks:
			if user_job in pending_tasks:
				# use flower to remove pending task:
				abort_response = CTSFlower().abortRunningTask(user_job)

		all_user_jobs = json.loads(redis_conn.get(sessionid))  # get all user's job ids

		for user_job in all_user_jobs:
			if user_job in user_jobs:
				# remove from redis cache, then remove from celery queue using flower:
				all_user_jobs.remove(user_job)

		# remove user's cache from redis, then set it again w/ remaining jobs:
		redis_conn.delete(sessionid)
		remaining_jobs = json.dumps(all_user_jobs)
		redis_conn.set(sessionid, remaining_jobs)

	except Exception as e:
		raise e