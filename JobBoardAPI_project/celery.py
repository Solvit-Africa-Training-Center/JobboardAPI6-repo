# myproject/celery.py

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JobBoardAPI_project.settings')

app = Celery('JobBoardAPI_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Optional: simple debug task to test Celery
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')