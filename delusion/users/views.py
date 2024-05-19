from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser
from django.core.mail import send_mail
from faker import Faker
from rest_framework.decorators import parser_classes
from .models import Anomaly, User, Node
import random
from .permissions import IsUserOrReadOnly
from .serializers import (
    CreateUserSerializer,
    UserSerializer,
    UserUpdateSerializer,
    NodeSerializer,
)

faker = Faker()


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

    def perform_create(self, serializer):
        data = serializer.validated_data

        data['description'] = faker.text()
        data['ip_address'] = faker.ipv4()
        data['mac_address'] = faker.mac_address()
        data['node_type'] = random.choices(['server', 'router', 'switch', 'firewall', 'storage'])
        data['status'] = random.choice(['active', 'inactive', 'maintenance'])
        data['os_version'] = random.choice(['Ubuntu 20.04', 'CentOS 8', 'Debian 10', 'Windows Server 2019', 'Windows 10', 'Windows 11', 'macOS', 'iOS', 'Android',])
        data['cpu_usage'] = round(random.uniform(0, 100), 2)
        data['memory_usage'] = round(random.uniform(0, 100), 2)
        data['disk_usage'] = round(random.uniform(0, 100), 2)
        data['uptime'] = f"{random.randint(1, 365)} days"

        serializer.save()

        if data['cpu_usage'] > 90 or data['memory_usage'] > 90 or data['disk_usage'] > 90:
            anomaly = Anomaly.objects.create(node=serializer.instance, description="High resource usage detected")
            send_anomaly_email(anomaly)


class NodeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = (AllowAny,)

class NodeRetrieveWithNodeIDView(generics.RetrieveAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'node_id'
    lookup_url_kwarg = 'node_id'


def send_anomaly_email(anomaly):
    subject = "Anomaly Detected"
    message = f"Anomaly detected on node {anomaly.node.name}: {anomaly.description}\nDetected at: {anomaly.detected_at}"
    sender = 'info@gmail.com'
    recipients = ['admin1@email.com', 'admin2@email.com']
    send_mail(subject, message, sender, recipients)
