from __future__ import absolute_import, unicode_literals
import os,sys
import django
from celery import Celery,platforms
from django.conf import settings

from celery.signals import task_prerun, task_postrun
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opensa.settings')
app = Celery('opensa')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.timezone = 'Asia/Shanghai'





