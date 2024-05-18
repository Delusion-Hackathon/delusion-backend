from rest_framework import permissions

from delusion.company.models import Ticket


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class CompanyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.workers.filter(user=request.user))


class IsAdminOrTicketOwner(permissions.BasePermission):
    """Only admin or ticket owner can perform actions on"""

    def has_permission(self, request, view):
        if request.user and  request.user.is_staff:
            return True

        if ticket_id := view.kwargs.get('pk'):
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                return ticket.sender == request.user
            except Ticket.DoesNotExist:
                pass
        
        return False


    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.sender == request.user
