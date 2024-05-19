from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from delusion.users.models import User, Node


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "ip_address",
        "node_type",
        "status",
    )
