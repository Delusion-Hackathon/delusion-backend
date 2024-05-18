from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from delusion.company.models import Message, Ticket

from ..users.models import MeshUser
from .services.company_services import (
    create_company,
    update_company,
    delete_company
)
from .serializers import (
    CompanySerializer,
    CreateCompanySerializer,
    DetailCompanySerialzier,
    TicetCloseSerializer,
    TicketSerializer,
    MessageSerializer
)
from .selectors import (
    all_companies,
    all_workers
)
from .permissions import (
    CompanyPermission,
    IsAdminOrTicketOwner
)


#== *************************  Company Views Start  ************************* ==#

class ListCompanyAPIView(generics.ListAPIView):
    """
    * A view that displays companies that match the user who sent the request.
    """

    queryset = all_companies()
    serializer_class = CompanySerializer
    permission_classes = [CompanyPermission]

    def get_queryset(self):
        company_ids = all_workers().filter(user=self.request.user).values_list('company', flat=True)
        qs = self.queryset.filter(id__in=company_ids, parent_company__isnull=True)
        return qs


class CreateCompanyAPIView(generics.CreateAPIView):
    """
    * A view for creating companies and their corresponding sub-companies.
    """

    queryset = all_companies()
    serializer_class = CreateCompanySerializer
    permission_classes = [CompanyPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mesh_obj = MeshUser.objects.filter(user=request.user).last()
        company = create_company(
            user=request.user,
            mesh_username=mesh_obj.mesh_username,
            mesh_password=mesh_obj.mesh_password,
            **serializer.validated_data
        )
        return Response({'detail': 'New company added'}, status=status.HTTP_201_CREATED)


class DetailCompanyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    * This view is used to `view`, `update` and `delete` relevant company information.
    """

    queryset = all_companies()
    serializer_class = DetailCompanySerialzier
    permission_classes = [CompanyPermission]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            company = update_company(instance, **serializer.validated_data)
            return Response({'detail': 'Company information updated'}, status=status.HTTP_200_OK)
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_company(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

#== *************************  Company Views End  ************************* ==#



#== *************************  Ticket Views Start  ************************* ==#
class TicketListCreateAPIView(generics.ListCreateAPIView):
    """
    * A view that displays tickets that match the user who sent the request.
    """

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(sender=self.request.user)


class TicketDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    * This view is used to `view` relevant ticket information.
    """

    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrTicketOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(sender=user)

    def get_serializer_class(self):
        if self.request.method in frozenset(['PUT', 'PATCH']):
            return TicetCloseSerializer
        return TicketSerializer

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({'detail': 'Ticket closed successfully'}, status=status.HTTP_200_OK)

class MessageListCreateAPIView(generics.ListCreateAPIView):
    """
    * A view that displays messages that match the user who sent the request.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTicketOwner]

    def get_queryset(self):
        ticket_id = self.kwargs['pk']
        try:
            return Message.objects.filter(ticket__id=ticket_id).order_by('-created_at')
        except Ticket.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        ticket_id = self.kwargs['pk']
        ticket = get_object_or_404(Ticket, id=ticket_id)
        serializer.save(ticket=ticket)
