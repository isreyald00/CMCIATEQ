from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlMetrologicoCIATEQ.settings')

app = Celery('ControlMetrologicoCIATEQ')

app.config_from_object('django.conf', namespace='CELERY')

app.conf.beat_schedule = {
    'cambiar_estatus_cal':{
        'task': 'calibracion.tasks.cambiar_estatus',
        'schedule': crontab(minutes=1)
    }
}

app.autodiscover_tasks()