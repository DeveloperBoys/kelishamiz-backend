from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from drf_yasg.openapi import Schema, Response as SwaggerResponse
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.schemas import ManualSchema
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.generics import GenericAPIView, UpdateAPIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .models import User
from .serializers import (ChangeUserInformationSerializer, UserLoginSerializer, VerifyRequestSerializer,
                          AdminLoginSerializer, LogoutSerializer, UserDataSerializer, CustomTokenRefreshSerializer)


class AdminLoginView(TokenObtainPairView):
    serializer_class = AdminLoginSerializer


class UserLoginView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def post(self, request):
        serializer = self.get_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class VerifyApiView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VerifyRequestSerializer

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        user = self.request.user
        self.check_verify(user, code)
        return Response(
            data={
                "success": True,
                "access": user.tokens()["access"],
                "refresh": user.tokens()["refresh"]
            }, status=200)

    @staticmethod
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def check_verify(user, code):
        verifies = user.verify_codes.filter(
            expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                'message': "Code is incorrect or expired"
            }
            user.delete()
            raise ValidationError(data)
        verifies.update(is_confirmed=True)
        user.save()
        return True


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                "success": True,
                "message": "You are logged out"
            }
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class UserDataView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDataSerializer

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request is not None:
            return User.objects.filter(self.request.user)
        return User.objects.none()


class ChangeUserInformationView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeUserInformationSerializer
    http_method_names = ['patch', 'put']

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        return Response(data={"detail": "Updated successfully"}, status=status.HTTP_200_OK)
