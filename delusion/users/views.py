from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from .models import CompanyRegistration, Country, User
from .permissions import IsUserOrReadOnly
from .serializers import CountrySerializer, CreateUserSerializer, RegistrationSerializer, UserSerializer, UserUpdateSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAdminUser,)


class CompanyRegistrationViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = CompanyRegistration.objects.all()
    serializer_class = RegistrationSerializer


class CountryViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = None


@parser_classes((MultiPartParser,))
class UserMeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.request.user
