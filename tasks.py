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

logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

app.conf.CELERY_ALWAYS_EAGER = True
app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

from celery.utils import LOG_LEVELS
app.conf.CELERYD_LOG_LEVEL = LOG_LEVELS['DEBUG']


@app.task
def startTESTTask(request_post):
	from test_cts import views
	from django.http import HttpRequest

	# wrap post in django request:
	request = HttpRequest()
	request.POST = request_post

	logging.info("Calling TEST request_manager")

	return views.request_manager(request)