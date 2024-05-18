from django.contrib import admin
from .models import Node


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id',
        'node_id',
        'company',
        'name',
        'domain',
        'host',
        'os_desc',
        'ip',
        'antivirus',
        'auto_update',
        'firewall'
    )
