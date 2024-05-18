from PIL import Image
import io
from django.core.files import File

from rest_framework.exceptions import ValidationError
from rest_framework import exceptions
from rest_framework import serializers
from delusion.company.validators import validate_file_extension, validate_file_mimetype
from delusion.users.serializers import UserSerializer
from delusion.utils.base_serializer import DynamicFieldsSerializer
from .selectors import (
    all_companies,
    all_workers
)
from .models import (
    Company,
    Message,
    MessageFile,
    Ticket,
    TicketFile,
)
from delusion.node.models import Node


#== *************************  Company Serializers Start  ************************* ==#

class BranchSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class SubCompanySerializer(DynamicFieldsSerializer):
    sub_companies = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class CompanySerializer(DynamicFieldsSerializer):
    sub_companies = SubCompanySerializer(many=True, read_only=True)

    class Meta:
        model = Company
        exclude = ('modified_at', )


class CreateCompanySerializer(DynamicFieldsSerializer):
    class Meta:
        model = Company
        fields = ('parent_company', 'name')

    def validate(self, attrs):
        parent_company = attrs.get('parent_company')
        user = self.context.get('request').user
        company_ids = all_workers().filter(user=user).values_list('company', flat=True)
        qs = all_companies().filter(id__in=company_ids, parent_company__isnull=True)

        if (parent_company) and (parent_company not in qs):
            raise ValidationError({'detail': 'The information you entered is incorrect'})
        return super().validate(attrs)


class DetailCompanySerialzier(DynamicFieldsSerializer):
    class Meta:
        model = Company
        exclude = ('modified_at', )

    def validate(self, attrs):
        parent_company = attrs.get('parent_company')
        user = self.context.get('request').user
        company_ids = all_workers().filter(user=user).values_list('company', flat=True)
        qs = all_companies().filter(id__in=company_ids, parent_company__isnull=True)

        if (parent_company) and (parent_company not in qs):
            raise ValidationError({'detail': 'The information you entered is incorrect'})
        return super().validate(attrs)

#== *************************  Company Serializers End  ************************* ==#


#== *************************  Ticket Serializers Start ************************* ==#

class TicketSerializer(serializers.ModelSerializer):
    """Serializers for ticket objects"""

    sender = UserSerializer(read_only=True)
    ticket_file = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False),
        required=False
    )

    class Meta:
        model = Ticket
        fields = (
            "id",
            "title",
            "body",
            "sender",
            "priority",
            "status",
            "activity_status",
            "assigned",
            "created_at",
            "modified_at",
            "ticket_file",
        )
        read_only_fields = ("status", "activity_status",)

    def validate_ticket_file(self, value):
        if len(value) > 3:
            raise serializers.ValidationError("You can upload a maximum of 3 files.") 

        for uploaded_file in value:
            validate_file_extension(uploaded_file)
            validate_file_mimetype(uploaded_file)

        return value

    def create(self, validated_data):
        user = self.context["request"].user
        ticket_files = validated_data.pop("ticket_file", [])

        ticket = Ticket(**validated_data)
        ticket.sender = user
        ticket.save()

        for uploaded_file in ticket_files:
            if uploaded_file.name.split(".")[-1] in ["jpg", "jpeg", "png"]:
                image = Image.open(uploaded_file)
                image = image.convert("RGB")

                max_width = 1024
                max_height = 1024

                image.thumbnail((max_width, max_height))

                image_io = io.BytesIO()
                image.save(image_io, format="JPEG")

                TicketFile.objects.create(ticket=ticket, file=File(image_io, name=uploaded_file.name))
            else:
                TicketFile.objects.create(ticket=ticket, file=uploaded_file)

        return ticket

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['ticket_file'] = [
            {
                'id': file.id,
                'file': file.file.url
            }
            for file in instance.ticket_files.all()
        ]
        return representation


class TicetCloseSerializer(serializers.ModelSerializer):
    """Serializers for ticket objects"""

    class Meta:
        model = Ticket
        fields = (
            "status",
            "activity_status"
        )
        read_only_fields = ("status", "activity_status",)

    def update(self, instance, validated_data):
        if not instance.status:
            raise exceptions.ValidationError("This ticket is already closed.")

        instance.status = False
        instance.activity_status = False
        instance.save()
        return instance

class MessageSerializer(serializers.ModelSerializer):
    """Serializers for message objects"""

    sender = UserSerializer(read_only=True)
    message_file = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False),
        required=False,
    )

    class Meta:
        model = Message
        fields = (
            "id",
            "ticket",
            "sender",
            "body",
            "created_at",
            "modified_at",
            "message_file",
        )
        read_only_fields = ("ticket", "created_at", "modified_at")

    def validate_message_file(self, value):
        if len(value) > 3:
            raise serializers.ValidationError("You can upload a maximum of 3 files.") 

        for uploaded_file in value:
            validate_file_extension(uploaded_file)
            validate_file_mimetype(uploaded_file)

        return value

    def create(self, validated_data):
        user = self.context["request"].user

        ticket = validated_data["ticket"]
        message_files = validated_data.pop("message_file", [])

        message = Message(**validated_data)
        message.sender = user
        message.save()

        if not ticket.status:
            raise serializers.ValidationError("You can't send message, ticket is closed.")

        for uploaded_file in message_files:
            MessageFile.objects.create(message=message, file=uploaded_file)

        if user.is_staff and ticket.activity_status:
            ticket.activity_status = False
            ticket.save()
        elif user == ticket.sender:
            ticket.activity_status = True
            ticket.save()

        return message

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['message_file'] = [
            {
                'id': file.id,
                'file': file.file.url
            }
            for file in instance.message_files.all()
        ]
        return representation
