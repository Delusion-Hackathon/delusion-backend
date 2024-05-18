from django.db import models


class AntiVirusChoices(models.TextChoices):
    LOW = 'l', 'Low'
    MEDIUM = 'm', 'Medium'
    HIGH = 'h', 'High'
