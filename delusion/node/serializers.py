from rest_framework import serializers
from delusion.utils.base_serializer import DynamicFieldsSerializer
from delusion.company.serializers import CompanySerializer
from .models import Node


#== *************************  Node Serializers Start  ************************* ==#

class NodeSerializer(DynamicFieldsSerializer):
    company = CompanySerializer(
        read_only=True, fields=['id', 'name', 'description', 'created_at']
    )

    class Meta:
        model = Node
        fields = '__all__'


class CreateNodeSerializer(DynamicFieldsSerializer):
    mesh_id = serializers.CharField(write_only=True, max_length=255)
    pc_users = serializers.ListField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Node
        fields = (
            'mesh_id', 'node_id', 'name', 'domain', 'host',
            'os_desc', 'ip', 'antivirus', 'auto_update', 'firewall',
            'pc_users'
        )


class DetailNodeSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Node
        fields = '__all__'

#== *************************  Node Serializers End  ************************* ==#
