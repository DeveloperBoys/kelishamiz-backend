from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate

from config.utility import check_user_type

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User


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


class UsersListSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="get_full_name", read_only=True)
    profileImageUrl = serializers.URLField(
        source="profile_image_url", read_only=True)
    isActive = serializers.BooleanField(source="is_active")
    dateJoined = serializers.DateTimeField(source="date_joined")

    class Meta:
        model = User
        fields = ['id', 'fullName', 'profileImageUrl',
                  'isActive', 'dateJoined']
        read_only_fields = ['id',]


class UsersSerializer(serializers.ModelSerializer):
    fistName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    fatherName = serializers.CharField(source="father_name", required=False)
    phoneNumber = serializers.CharField(source="phone_number")
    birthDate = serializers.DateField(source="birth_date", required=False)
    profileImageUrl = serializers.URLField(
        source="profile_image_url", read_only=True)
    isActive = serializers.BooleanField(source="is_active")
    profileImage = serializers.FileField(source="profile_image")
    userRoles = serializers.CharField(source="user_roles")
    authType = serializers.CharField(source="auth_type")
    dateJoined = serializers.DateTimeField(source="date_joined")

    class Meta:
        model = User
        fields = ['id', 'fistName', 'lastName', 'isActive', 'fatherName', 'phoneNumber', 'email',
                  'birthDate', 'profileImageUrl', 'profileImage', 'userRoles', 'authType', 'dateJoined']
        read_only_fields = ['id',]
