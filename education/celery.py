from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education.settings')
django.setup()

app = Celery('education')
# app = Celery('education',
#     backend=settings.BACKEND_URL,
#     broker=settings.BROKER_URL,
#     result=settings.CELERY_RESULT_BACKEND)


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
