from __future__ import absolute_import
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebooking.settings')


RUN_DOCKERIZED = os.environ.get('RUN_DOCKERIZED')

REDIS_HOST = 'redis' if RUN_DOCKERIZED else '127.0.0.1'
REDIS_HOST = '0.0.0.0'
# REDIS_PASSWD = 'lruPYlSfRqeh-meq-21Z1fsxK6c'
# REDIS_PORT = 6379

# # broker_url = f'redis://:{REDIS_PASSWD}@{REDIS_HOST}:{REDIS_PORT}' if REDIS_PASSWD else f'redis://{REDIS_HOST}:{REDIS_PORT}'
# CELERY_BROKER_REDIS_URL= f'redis://:{REDIS_PASSWD}@host.docker.internal:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'


class CeleryConfig:
    enable_utc = True
    timezone = 'Europe/Bucharest'
    broker_url = CELERY_RESULT_BACKEND
    backend_url = CELERY_RESULT_BACKEND
    imports = ('reservation.tasks', 'accounts.utils')


app = Celery(namespace='ebooking')
app.config_from_object(CeleryConfig)
app.autodiscover_tasks()