"""
CTS celery instance
"""
from __future__ import absolute_import
import os
from celery import Celery
import logging

# if not os.environ.get('DJANGO_SETTINGS_MODULE'):
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
#     # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_apache')

try:
    from celery_cts import settings_local
except ImportError:
    logging.info("could not import settings_local in celery_cts")
    pass


if not os.environ.get('REDIS_HOSTNAME'):
    os.environ.setdefault('REDIS_HOSTNAME', 'localhost')

REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME')

logging.warning("REDIS HOSTNAME: {}".format(REDIS_HOSTNAME))

# app = Celery('celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app = Celery(broker='redis://{}:6379/0'.format(REDIS_HOSTNAME),	
             backend='redis://{}:6379/0'.format(REDIS_HOSTNAME),
             include=['celery_cts.tasks'])

app.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)

logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
