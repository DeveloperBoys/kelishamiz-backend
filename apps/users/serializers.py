from drf_yasg.openapi import Schema

from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from config.utility import check_phone, check_user_type
from .utils import phone_parser
from .tasks import send_phone_notification
from .models import User


class VerifyRequestSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class AdminLoginSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super(AdminLoginSerializer, self).__init__(*args, **kwargs)
        self.fields['userInput'] = serializers.CharField(required=True)
        self.fields['username'] = serializers.CharField(
            read_only=True, required=False)

    def auth_validate(self, attrs):
        user_input = attrs.get('userInput')
        print(user_input)
        if check_user_type(user_input) == "username":
            username = attrs.get('userInput')
        elif check_user_type(user_input) == "email":
            user = self.get_user(email__iexact=user_input)
            username = user.username
        elif check_user_type(user_input) == "phone":
            user = self.get_user(phone_number=user_input)
            username = user.username
        else:
            data = {
                'success': False,
                'message': "You must send username or email or phone number"
            }
            return ValidationError(data)
        authentication_kwargs = {
            self.username_field: username,
            'password': attrs['password']
        }
        user = authenticate(**authentication_kwargs)
        if user is not None:
            self.user = user
        else:
            raise ValidationError(
                {"password": "Sorry, login or password you entered is incorrect. Please check and try again."}
            )

    def validate(self, attrs):
        self.auth_validate(attrs)
        data = self.user.tokens()
        return data

    def get_user(self, **kwargs):
        users = User.objects.filter(**kwargs)
        if not users.exists():
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                "no_active_account",
            )
        return users.first()


class UserLoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, phone_number):

        if check_phone(phone_number) == "phone":
            phone_parser(phone_number, self.initial_data.get("country_code"))

        return phone_number

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        user, created = self.get_or_create_user(phone_number)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        data = {
            'refresh': str(refresh),
            'access': str(access_token),
        }

        if created:
            data['new_user'] = True
        else:
            data['new_user'] = False

        return data

    def get_or_create_user(self, phone_number):
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            user.set_unusable_password()
            user.save()
        code = user.create_verify_code()
        send_phone_notification.delay(user.phone_number, code)
        return user, created


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.context['request'].data.get('refresh')
        data['refresh'] = refresh

        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user)

        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        help_text="The refresh token obtained during login.",
        label="Refresh Token",
        required=True
    )


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'father_name',
                  'email', 'phone_number', 'birth_date')


class ChangeUserInformationSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    father_name = serializers.CharField(
        write_only=True, required=False, allow_null=True)
    email = serializers.EmailField(write_only=True, required=True)
    phone_number = serializers.CharField(write_only=True, required=True)
    birth_date = serializers.DateField(
        write_only=True, required=False, allow_null=True)

    def validate_phone_number(self, phone_number):
        if not check_phone(phone_number):
            raise ValidationError("Invalid phone number format.")

        user = self.context['request'].user
        query = Q(phone_number=phone_number) & ~Q(pk=user.pk)
        if User.objects.filter(query).exists():
            raise serializers.ValidationError(
                "Phone number already in use by a verified user.")

        return phone_number

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.father_name = validated_data.get(
            'father_name', instance.father_name)
        instance.email = validated_data.get('email', instance.email)
        instance.birth_date = validated_data.get(
            'birth_date', instance.birth_date)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)

        instance.save()
        return instance
