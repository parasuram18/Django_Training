import os
from celery import Celery
from django.conf import settings
# set django's default settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
# broker_connection_retry_on_startup = True

app = Celery('main')


app.config_from_object('django.conf:settings', namespace='CELERY')

# load task from all registered django apps
app.autodiscover_tasks()