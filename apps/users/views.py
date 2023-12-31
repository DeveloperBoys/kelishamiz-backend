from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import GenericAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, RetrieveDestroyAPIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from apps.classifieds.models import Classified
from apps.user_searches.models import SearchQuery
from apps.admin_api.filters import ClassifiedFilter
from apps.user_searches.serializers import SearchQuerySerializer
from apps.classifieds.serializers import ClassifiedListSerializer, ClassifiedSerializer
from .serializers import (ChangeUserInformationSerializer, UserLoginSerializer, VerifyRequestSerializer,
                          LogoutSerializer, UserDataSerializer, CustomTokenRefreshSerializer)


@method_decorator(cache_page(60*60*2), name='dispatch')
class UserLoginView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@method_decorator(cache_page(60*60*2), name='dispatch')
class VerifyApiView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VerifyRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
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


# @method_decorator(cache_page(60*60*2), name='dispatch')
class UserDataView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDataSerializer

    def get_object(self):
        return self.request.user

    @action(detail=True, methods=['GET', 'DELETE'], url_path="searches/", url_name="user-searches")
    def user_searches(self, request, *args, **kwargs):
        searches = SearchQuery.objects.filter(user=self.get_object())
        serializer = SearchQuerySerializer(searches, many=True)
        return Response(serializer.data)


class UserClassifiedListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClassifiedListSerializer
    filterset_class = ClassifiedFilter

    def get_queryset(self):
        return Classified.objects.filter(owner=self.request.user)


class UserClassifiedDetailView(RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClassifiedSerializer

    def get_queryset(self):
        return Classified.objects.filter(owner=self.request.user, pk=self.kwargs['pk'])


class UserSearchesView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SearchQuerySerializer
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user:
            return SearchQuery.objects.filter(user=user)
        return []


@method_decorator(cache_page(60*60*2), name='dispatch')
class ChangeUserInformationView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeUserInformationSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(data={"detail": "Updated successfully"}, status=status.HTTP_200_OK)


class LikedClassifiedsView(ListAPIView):
    """
    Returns classifieds liked by authenticated user
    """
    serializer_class = ClassifiedListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Classified.objects.filter(
            classifiedlike__user=user,
            classifiedlike__is_active=True
        )
