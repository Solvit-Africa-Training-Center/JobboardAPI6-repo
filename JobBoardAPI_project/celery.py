# myproject/celery.py

import os
from celery import Celery
from django.conf import settings

# Set default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JobBoardAPI_project.settings')

# Create Celery app instance
app = Celery('SendingCeleryEmail')

# Load settings from Django settings.py using CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Optional: simple debug task to test Celery
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')