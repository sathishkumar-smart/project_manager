# config/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('project_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'daily_summary_email': {
        'task': 'projects.tasks.send_daily_summary_email',
        'schedule': crontab(minute='*/1'),
        'args': (),
    },
}