"""Users serializers."""

# Django
from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from software_challenge_api.users.models import User

# Utilities
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )



class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle the user registration request data and validation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        min_length=4,
        max_length=20
    )

    # password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError({
                'password_confirmation': 'Passwords don\'t match.'
            })
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation"""
        data.pop('password_confirmation')
        try:
            user = User.objects.create_user(**data)
        except IntegrityError:
            raise serializers.ValidationError('Username or Email already exists.')
        return user


class UserLoginSerializer(serializers.Serializer):
    """User Login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Validate the information of the login user"""
        user = authenticate(username=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Please check your username and password and try again.')
        self.context['user'] = user

        return data

    def create(self, data):
        """Create token for identificate the user and update the last login date"""
        token, created_token = Token.objects.get_or_create(user=self.context['user'])

        user = self.context['user']
        if created_token:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
        return user, token.key
