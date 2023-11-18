from django.db.models import Q
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .models import User
# from .tasks import send_phone_notification
from config.utility import check_phone
from apps.likes.models import ClassifiedLike
from apps.classifieds.models import Classified
from apps.user_searches.models import SearchQuery
from .utils import phone_parser, send_phone_notification
from apps.user_searches.serializers import SearchQuerySerializer
from apps.classifieds.serializers import ClassifiedListSerializer


class VerifyRequestSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class UserLoginSerializer(serializers.Serializer):

    phoneNumber = serializers.CharField(required=True)

    def validate_phoneNumber(self, phone_number):

        if check_phone(phone_number) == "phone":
            phone_parser(phone_number, self.initial_data.get("country_code"))

        return phone_number

    def validate(self, attrs):
        phone_number = attrs.get('phoneNumber')
        user, created = self.get_or_create_user(phone_number)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        data = {
            'refresh': str(refresh),
            'access': str(access_token),
        }

        if created:
            data['newUser'] = True
        else:
            data['newUser'] = False

        return data

    def get_or_create_user(self, phone_number):
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            user.set_unusable_password()
            user.save()
        code = user.create_verify_code()
        # send_phone_notification.delay(user.phone_number, code)
        send_phone_notification(user.phone_number, code)
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
    firstName = serializers.CharField(source='first_name', required=True)
    lastName = serializers.CharField(source='last_name', required=True)
    profileImage = serializers.FileField(source='father_name', required=False)
    fatherName = serializers.CharField(source='first_name', required=False)
    phoneNumber = serializers.CharField(source='phone_number', required=True)
    birthDate = serializers.CharField(source='birth_date', required=False)

    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'fatherName', 'email', 'phoneNumber',
                  'birthDate', 'profileImage']
        read_only_fields = ['id']


class ChangeUserInformationSerializer(serializers.Serializer):
    firstName = serializers.CharField(write_only=True, required=True)
    lastName = serializers.CharField(write_only=True, required=True)
    profileImage = serializers.FileField(write_only=True, required=False)
    fatherName = serializers.CharField(
        write_only=True, required=False, allow_null=True)
    email = serializers.EmailField(write_only=True, required=True)
    phoneNumber = serializers.CharField(write_only=True, required=True)
    birthDate = serializers.DateField(
        write_only=True, required=False, allow_null=True)

    def validate_phoneNumber(self, phone_number):
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
            'firstName', instance.first_name)
        instance.last_name = validated_data.get(
            'lastName', instance.last_name)
        instance.father_name = validated_data.get(
            'fatherName', instance.father_name)
        instance.email = validated_data.get('email', instance.email)
        instance.birth_date = validated_data.get(
            'birthDate', instance.birth_date)
        instance.phone_number = validated_data.get(
            'phoneNumber', instance.phone_number)
        instance.profile_image = validated_data.get(
            'profileImage', instance.profile_image
        )

        instance.save()
        return instance
