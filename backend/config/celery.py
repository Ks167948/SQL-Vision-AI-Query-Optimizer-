import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('sql_vision')

# Read config from Django settings, the CELERY namespace means 
# settings must start with CELERY_ (e.g., CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()