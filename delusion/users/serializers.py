from rest_framework import serializers
from delusion.users.models import User, Node


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )
        read_only_fields = ("username",)


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ("id", "username", "password", "first_name", "last_name", "email")
        extra_kwargs = {"password": {"write_only": True}, "email": {"required": True}}


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_picture",
        )
        extra_kwargs = {"username": {"required": False}}


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
