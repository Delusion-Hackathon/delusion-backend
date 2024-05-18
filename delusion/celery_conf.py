import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delusion.config.local")

from celery import Celery
from configurations import importer


importer.install()

app = Celery("delusion")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()



