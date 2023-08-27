from datetime import datetime

from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .utils import send_email, send_phone_notification
from .serailizers import (ChangeUserInformationSerializer, MyTokenObtainPairSerializer,
                          CustomTokenRefreshSerializer, LogoutSerializer, SignUpSerializer)
from .models import User, CODE_VERIFIED, DONE, VIA_SOCIAL, VIA_PHONE


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': True,
                "message": "You are logged out"
            }
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerializer


class VerifyApiView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user, code = self.request.user, request.data.get('code')
        # user = self.request.user
        # code = self.request.data.get('code')
        self.check_verify(user, code)
        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                "access": user.tokens()["access"],
                "refresh": user.tokens()["refresh"]
            }, status=200)

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(
            expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                'message': "Code is incorrect or expired"
            }
            raise ValidationError(data)
        verifies.update(is_confirmed=True)
        if user.auth_status not in DONE:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class GetNewVerification(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        # if user.auth_type == VIA_EMAIL:
        #     code = user.create_verify_code(VIA_EMAIL)
        # send_email(user.email, code)
        if user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_phone_notification(user.phone_number, code)
        else:
            data = {
                "message": "You need to enter email or phone_number",
            }
            raise ValidationError(data)
        return Response(
            {
                "success": True
            }
        )

    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(
            expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                "message": "You need to wait over expiration time",
            }
            raise ValidationError(data)


class ChangeUserView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChangeUserInformationSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserView, self).partial_update(request, *args, **kwargs)

        return Response(
            data={
                "detail": "Updated successfully",
                "auth_status": self.request.user.auth_status,
            }, status=200
        )
