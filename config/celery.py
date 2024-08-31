import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("camp-python-2024-codearena-backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
