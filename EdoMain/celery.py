import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EdoMain.settings')

app = Celery('EdoMain')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'processing-database-1': {
        'task': 'Pages.tasks.processing_database',
        'schedule': crontab(minute=0, hour=1),
    }
}
