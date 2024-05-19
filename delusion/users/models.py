from django.db import models
from django.contrib.auth.models import AbstractUser
from delusion.users.choices import NodeChoices, StatusChoices


class User(AbstractUser):
    # TODO: add default profile picture
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )

    def __str__(self):
        return self.username

class Node(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(unique=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    node_type = models.CharField(
        max_length=255, choices=NodeChoices.choices, default=NodeChoices.ROUTER
    )
    status = models.CharField(
        max_length=255, choices=StatusChoices.choices, default=StatusChoices.ACTIVE
    )
    location_x = models.CharField(max_length=255, blank=True, null=True)
    location_y = models.CharField(max_length=255, blank=True, null=True)

    os_version = models.CharField(max_length=255, blank=True, null=True)
    cpu_usage = models.FloatField(blank=True, null=True)
    memory_usage = models.FloatField(blank=True, null=True)
    disk_usage = models.FloatField(blank=True, null=True)
    uptime = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
