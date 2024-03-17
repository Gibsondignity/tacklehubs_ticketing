# path/to/your/proj/src/cfehome/celery.py
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyrentproject.settings')


app = Celery('easyrentproject')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'verify-payments-every-30-minutes': {
        'task': 'dashboard.task.verify_all_payment',
        'schedule': crontab(minute='*/30'),
    },
}

app.autodiscover_tasks() 
