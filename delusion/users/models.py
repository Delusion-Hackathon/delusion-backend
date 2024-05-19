from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # TODO: add default profile picture
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )

    def __str__(self):
        return self.username


class Node(models.Model):
    node_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    node_type = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    position_x = models.CharField(max_length=255, blank=True, null=True)
    position_y = models.CharField(max_length=255, blank=True, null=True)

    os_version = models.CharField(max_length=255, blank=True, null=True)
    cpu_usage = models.FloatField(blank=True, null=True)
    memory_usage = models.FloatField(blank=True, null=True)
    disk_usage = models.FloatField(blank=True, null=True)
    uptime = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Anomaly(models.Model):
    anomaly_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="anomalies")
    description = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anomaly {self.anomaly_id} on {self.node.name}"
