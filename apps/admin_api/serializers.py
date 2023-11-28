from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate

from apps.users.models import User
from config.utility import check_user_type
from apps.payments.models import UserBalance
from apps.classifieds.serializers import ClassifiedDetailSerializer
from apps.classifieds.models import Classified, ClassifiedDetail, ClassifiedImage

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
    balance = serializers.SerializerMethodField()
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
                  'birthDate', 'profileImageUrl', 'balance', 'profileImage', 'userRoles', 'authType', 'dateJoined']
        read_only_fields = ['id',]

    def get_balance(self, obj):
        user_balance = UserBalance.objects.filter(user=obj).last()
        if user_balance:
            return user_balance.balance
        return None


class UserClassifiedsSerializer(serializers.ModelSerializer):
    detail = ClassifiedDetailSerializer()
    createdAt = serializers.DateTimeField(source='created_at')
    updatedAt = serializers.DateTimeField(source='updated_at')
    category = serializers.SerializerMethodField()

    class Meta:
        model = Classified
        fields = ('id', 'title', 'category', 'status',
                  'detail', 'createdAt', 'updatedAt')
        read_only_fields = ('id',)

    def get_category(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            return obj.category.name
        return obj.category.pk

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.category.pk = validated_data.get(
            'category', instance.category.pk)
        instance.save()

        detail_data = validated_data.get('detail', {})
        detail_serializer = ClassifiedDetailSerializer(
            instance=instance.classifieddetail, data=detail_data, partial=True
        )
        if detail_serializer.is_valid():
            detail_serializer.save()

        return instance


class UserClassifiedListSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Classified
        fields = ('id', 'category', 'owner', 'title',
                  'status', 'imageUrl', 'createdAt')
        read_only_fields = ('id',)

    def get_price(self, obj):
        classified_detail = ClassifiedDetail.objects.filter(
            classified=obj).first()
        return classified_detail.price if classified_detail else None

    def get_category(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            return obj.category.name
        return obj.category.pk

    def get_imageUrl(self, obj):
        classified_image = ClassifiedImage.objects.filter(
            classified=obj).first()
        return classified_image.image_url if classified_image else None
