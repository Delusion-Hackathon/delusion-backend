from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from .models import User, Node
from .permissions import IsUserOrReadOnly
from .serializers import (
    CreateUserSerializer,
    UserSerializer,
    UserUpdateSerializer,
    NodeSerializer,
)


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    Updates and retrieves user accounts
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Creates user accounts
    """

    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAdminUser,)


@parser_classes((MultiPartParser,))
class UserMeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.request.user


class NodeListCreateView(generics.ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = (AllowAny,)


class NodeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = (AllowAny,)
