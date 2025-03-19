from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """serializer class"""

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'created', 'updated')


class AuthSerializer(serializers.Serializer):
    """serializer class"""

    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, data):
        username = data.get('username').lower()
        password = data.get('password')

        if username and password:
            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError(
                    _('Unable to log in with provided credentials.'),
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                _('Must include both "username" and "password".'),
                code='authorization'
            )

        data['user'] = user
        return data


class LogoutSerializer(serializers.Serializer):
    """Serializer class"""
    refresh_token = serializers.CharField()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """serializer class
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Confirm password")

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove password2 from the validated data since we don't need it anymore
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'].lower(),
            email=validated_data['email'].lower(),
            password=validated_data['password']
        )
        return user


