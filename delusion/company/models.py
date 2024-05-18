import os
from PIL import Image

from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from delusion.company.choices import AssignedChoices, TicketPriority
from delusion.company.validators import validate_file_mimetype
from delusion.utils.models import TrackingModel


USER = get_user_model()


class Company(TrackingModel):
    mesh_id = models.CharField(max_length=255, unique=True, blank=True)
    username = models.CharField(max_length=64, unique=True, null=True, blank=True)
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='uploads/company/'
    )
    parent_company = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_companies')

    @property
    def get_mesh_id(self):
        return self.mesh_id.replace('mesh//', '', 1)

    def delete(self):
        if (self.is_active):
            self.is_active = False
            self.save()
        else:
            raise ValidationError({'detail': 'Not found.'})

    class Meta:
        db_table = 'company'
        ordering = ('-pk', )
        verbose_name_plural = 'Companies'


class Worker(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='workers')
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='workers')

    class Meta:
        db_table = 'worker'
        ordering = ('-pk', )

class BaseFile(TrackingModel):
    file = models.FileField(
        upload_to='uploads/ticket/',
        validators=[
            FileExtensionValidator(['pdf', 'jpg', 'png', 'jpeg', 'txt', "log"]),
            validate_file_mimetype,
        ],
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

class Ticket(TrackingModel):
    """Model definition for Tickets."""

    title = models.CharField("title", max_length=128)
    body = models.TextField("body")
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="sender",
        related_name="tickets",
    )
    assigned = models.CharField(
        "assigned",
        max_length=1,
        choices=AssignedChoices.choices,
    )
    priority = models.CharField(
        "priority",
        max_length=1,
        choices=TicketPriority.choices,
    )
    activity_status = models.BooleanField("activity status", default=True)
    status = models.BooleanField("status", default=True)

    class Meta:
        verbose_name = "ticket"
        verbose_name_plural = "tickets"
        db_table = "tickets"

    def __str__(self) -> str:
        return f"SupportRequest(sender:{self.sender}, subject:{self.title})"

    def __repr__(self) -> str:
        return f"SupportRequest(sender:{self.sender}, subject:{self.title})"

class TicketFile(BaseFile):
    ticket = models.ForeignKey(
        "company.Ticket",
        on_delete=models.CASCADE,
        related_name='ticket_files',
        verbose_name="ticket",
    )

    def __str__(self):
        return f"TicketFile for Ticket {self.ticket.id}"

class Message(TrackingModel):
    """Model definition for Messages."""

    ticket = models.ForeignKey(
        "company.Ticket",
        on_delete=models.CASCADE,
        verbose_name="ticket",
        related_name="messages",
        blank=True,
        null=True,
    )
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="sender",
        related_name="messages",
    )
    body = models.TextField("body")

    class Meta:
        verbose_name = "message"
        verbose_name_plural = "messages"
        db_table = "messages"

    def __str__(self) -> str:
        return f"Message(sender:{self.sender}, ticket:{self.ticket})"

    def __repr__(self) -> str:
        return f"Message(sender:{self.sender}, ticket:{self.ticket})"

class MessageFile(BaseFile):
    message = models.ForeignKey(
        "company.Message",
        on_delete=models.CASCADE,
        related_name='message_files',
        verbose_name="message",
    )

    def __str__(self):
        return f"MessageFile for Message {self.message.id}"
