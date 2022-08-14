from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo_project.settings")

app = Celery("todo_project")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

CELERY_BEAT_SCHEDULE = {
    'send_email_every_morning_celery': {
        'task': 'accounts.tasks.send_email_every_morning_celery',
        'schedule': crontab(hour=8, minute=0),
    },
    'send_email_every_week_celery': {
        'task': 'accounts.tasks.send_email_every_week_celery',
        'schedule': crontab(day_of_week=6, hour=9, minute=0),
    },
}
