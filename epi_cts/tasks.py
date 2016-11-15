from __future__ import absolute_import

import importlib
import os
from celery import Celery
import logging


if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_apache')

if not os.environ.get('REDIS_HOSTNAME'):
    os.environ.setdefault('REDIS_HOSTNAME', 'localhost')

REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME')

# app = Celery('celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app = Celery(broker='redis://{}:6379/0'.format(REDIS_HOSTNAME),
             backend='redis://{}:6379/0'.format(REDIS_HOSTNAME),
             include=['celery_cts.tasks'])

app.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    # CELERYD_NODES=6,
    # CELERY_BIN="/var/www/ubertool/virtualenv/bin/celery",
    # CELERY_APP="tasks:app",
    # CELERYD_CHDIR="/var/www/ubertool/ubertool_cts",
    # CELERYD_USER="celery",
    # CELERYD_GROUP="celery",
    # CELERY_CREATE_DIRS=1,
    # %N will be replaced with the first part of the nodename.
    # CELERYD_LOG_FILE="/var/log/celery/%n.log",
    # CELERYD_PID_FILE="/var/run/celery/%n.pid",
    # CELERYD_LOG_FILE="%n.log",
    # CELERYD_PID_FILE="%n.pid",
)

logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)


# @shared_task
@app.task
def startCalcTask(calc, request_post):
    from django.http import HttpRequest

    # TODO: try catch that works with celery task, for retries...

    calc_views = importlib.import_module('.views', calc + '_cts')  # import calculator views

    # wrap post in django request:
    request = HttpRequest()
    request.POST = request_post

    logging.info("Calling {} request_manager as celery task!".format(calc))

    return calc_views.request_manager(request)
