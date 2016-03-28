from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
import logging


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_local')
# settings.configure()

app = Celery('cts_tasks', broker='redis://localhost:6379/0')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def startTESTTask(request_post):
	from test_cts import views
	from django.http import HttpRequest

	# wrap post in django request:
	request = HttpRequest()
	request.POST = request_post

	logging.info("Calling TEST request_manager")

	return views.request_manager(request)