from rest_framework.permissions import BasePermission
from django.conf import settings


class Check_API_KEY_Auth(BasePermission):
    def has_permission(self, request, view):
        api_key_secret = request.headers.get('Api-Key')
        return api_key_secret == settings.API_KEY_SECRET
