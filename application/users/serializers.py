from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

from project.exceptions import ConflictError

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'email', 'first_name', 'last_name', 'password')
        read_only_fields = ('uuid',)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ConflictError(detail=_('Email already in use.'))

        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class TokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, allow_blank=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Token
        fields = ('key', 'email', 'password')
        read_only_fields = ('key',)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise AuthenticationFailed()

        return value

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()

        if not user or not user.check_password(attrs['password']):
            raise AuthenticationFailed()

        attrs['user'] = user

        return attrs

    def create(self, validated_data):
        token, _ = Token.objects.get_or_create(user=validated_data['user'])

        return token
