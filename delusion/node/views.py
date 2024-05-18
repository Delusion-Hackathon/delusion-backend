from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import (
    NodeSerializer,
    CreateNodeSerializer,
    DetailNodeSerializer
)
from .permissions import Check_API_KEY_Auth
from .selectors import all_nodes
from .services.node_services import (
    get_url,
    create_node
)
from . import LB


#== *************************  Download Agent Views Start  ************************* ==#

class GetCommandAPIView(APIView):
    """
    * The endpoint that issues the command to `download the agent`.
    """

    def get(self, request, company_name):
        option = LB
        node_url = get_url(user=request.user, option=option, company_name=company_name)
        return Response({'detail': node_url}, status=status.HTTP_200_OK)


class DownloadAgentAPIView(APIView):
    """
    * An endpoint to `load a new agent`.
    """

    def get(self, request, option, company_name):
        node_url = get_url(user=request.user, option=option, company_name=company_name)
        return redirect(node_url)

#== *************************  Download Agent Views End  ************************* ==#


#== *************************  Node Views Start  ************************* ==#

class CreateNodeAPIView(generics.CreateAPIView):
    """
    * A view that creates a `node object` based on the sent data that also stores the `remote computer's data`.
    """

    queryset = all_nodes()
    serializer_class = CreateNodeSerializer
    permission_classes = [Check_API_KEY_Auth]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        node_obj = create_node(user=request.user, **serializer.validated_data)
        return Response({'detail': 'New node created successfully'}, status=status.HTTP_201_CREATED)

#== *************************  Node Views End  ************************* ==#
