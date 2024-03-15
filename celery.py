# path/to/your/proj/src/cfehome/celery.py
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyrentproject.settings')


app = Celery('easyrentproject')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks() 
