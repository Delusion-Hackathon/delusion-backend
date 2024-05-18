from rest_framework import serializers
from delusion.users.models import CompanyRegistration, Country, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)
        read_only_fields = ('username', )


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}, 'email': {"required": True}}


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):

    approved = serializers.ReadOnlyField()

    class Meta:
        model = CompanyRegistration
        fields = "__all__"


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'msp_name', 'profile_picture',)
        extra_kwargs = {'username': {"required": False}}
