import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bible_quiz_project.settings')

app = Celery('bible_quiz_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related config keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# 4. Cron / Beat Configuration
# Schedule the reminder task to run every day at 8:00 AM
app.conf.beat_schedule = {
    'send-daily-reminder-at-8am': {
        'task': 'quiz_api.tasks.send_daily_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
}