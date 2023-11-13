from rest_framework.filters import SearchFilter
from rest_framework import viewsets, permissions


from rest_framework_simplejwt.views import TokenObtainPairView

from django_filters.rest_framework import DjangoFilterBackend

from apps.users.models import User
from apps.classifieds.models import Classified
from .filters import UserFilter, ClassifiedFilter
from apps.user_searches.models import SearchQuery
from apps.user_searches.serializers import SearchQuerySerializer
from .serializers import (
    UsersSerializer,
    UsersListSerializer,
    AdminLoginSerializer,
    UserClassifiedsSerializer,
    UserClassifiedListSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    permission_classes = [permissions.IsAdminUser,]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['first_name']
    filterset_class = UserFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UsersSerializer
        return self.serializer_class


class UserClassifiedsViewSet(viewsets.ModelViewSet):
    queryset = Classified.objects.all()
    serializer_class = UserClassifiedListSerializer
    permission_classes = [permissions.IsAdminUser,]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ClassifiedFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserClassifiedsSerializer
        return self.serializer_class


class UserSearchViewSet(viewsets.ModelViewSet):
    serializer_class = SearchQuerySerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_queryset(self):
        try:
            user = self.kwargs['user_pk']
            return SearchQuery.objects.filter(user=user)
        except:
            return None


class AdminLoginView(TokenObtainPairView):
    serializer_class = AdminLoginSerializer


class ClassifiedsViewSet(viewsets.ModelViewSet):
    serializer_class = UserClassifiedListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    permission_classes = [permissions.IsAdminUser,]

    def get_queryset(self):
        try:
            user = self.kwargs['user_pk']
            if user:
                return Classified.objects.filter(owner=user)
            return None
        except:
            return None

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserClassifiedsSerializer
        return self.serializer_class


class LikedClassifiedsViewSet(viewsets.ModelViewSet):
    serializer_class = UserClassifiedListSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']
    permission_classes = [permissions.IsAdminUser,]

    def get_queryset(self):
        try:
            user = self.kwargs['user_pk']
            if user:
                return Classified.objects.filter(
                    classifiedlike__user=user,
                    classifiedlike__is_active=True
                ).prefetch_related('classifiedlike_set')
            return None
        except:
            return None

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserClassifiedsSerializer
        return self.serializer_class
