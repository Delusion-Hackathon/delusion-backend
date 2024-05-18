from django.db import models


class TicketPriority(models.TextChoices):
    LOW = 'l', 'Low'
    MEDIUM = 'm', 'Medium'
    HIGH = 'h', 'High'

class AssignedChoices(models.TextChoices):
    TECHNICIAN = 't', 'Technician'
    MANAGER = 'm', 'Manager'
