from __future__ import absolute_import
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebooking.settings')


class CeleryConfig:
    enable_utc = True
    timezone = 'Europe/Bucharest'
    broker_url = 'redis://:abcd12!!@127.0.0.1:6379'
    imports = ('hotels.tasks',)


app = Celery(namespace='ebooking')
app.config_from_object(CeleryConfig)
app.autodiscover_tasks()