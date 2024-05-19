import os
from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    def __init__(self) -> None:
        print("local")
        super().__init__()

    DEBUG = True
    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ("django_nose",)
    TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
    NOSE_ARGS = [
        BASE_DIR,
        "-s",
        "--nologcapture",
        "--with-coverage",
        "--with-progressive",
        "--cover-package=delusion",
    ]

    # Mail
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    from datetime import timedelta
    from celery.schedules import crontab

    CELERY_BEAT_SCHEDULE = {
        "sample_task": {
            "task": "delusion.tasks.check_ticket_status",
            "schedule": crontab(hour=12),
        },
    }
