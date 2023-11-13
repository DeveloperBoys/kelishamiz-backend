from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.filters import SearchFilter
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from .filters import ClassifiedFilter
from apps.user_searches.models import SearchQuery
from .models import (
    APPROVED,
    Category,
    Classified,
    ClassifiedImage,
    ClassifiedDetail,
)
from apps.permissions.permissions import (
    ClassifiedOwner,
    IsAdminOrReadOnly,
    DraftClassifiedPermission,
    PublishedClassifiedPermission
)
from .serializers import (
    CategorySerializer,
    ClassifiedListSerializer,
    ClassifiedSerializer,
    ClassifiedImageSerializer,
    CreateClassifiedSerializer,
    DeleteClassifiedSerializer,
    CreateClassifiedImageSerializer,
    CreateClassifiedDetailSerializer
)


class ClassifiedPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


@method_decorator(cache_page(60*15), name='dispatch')
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


@method_decorator(cache_page(60*15), name='dispatch')
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


@method_decorator(cache_page(60*15), name='dispatch')
class ClassifiedListView(generics.ListAPIView):
    queryset = Classified.objects.filter(
        status=APPROVED).order_by('-created_at')
    serializer_class = ClassifiedListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_class = ClassifiedFilter
    pagination_class = ClassifiedPagination

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        search_query = self.request.query_params.get('search')
        if search_query and self.request.user.is_authenticated:
            SearchQuery.objects.create(
                user=self.request.user,
                query=search_query
            )

        return queryset

    def list(self, request):
        page = request.query_params.get('page')

        if not page:
            queryset = self.queryset[:8]
        else:
            self.pagination = self.pagination_class
            queryset = self.queryset[8:]

        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


@method_decorator(cache_page(60*15), name='dispatch')
class ClassifiedDetailView(generics.ListAPIView):
    queryset = Classified.objects.filter(status=APPROVED)
    serializer_class = ClassifiedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]


@method_decorator(cache_page(60*15), name='dispatch')
class DeleteClassifiedView(generics.DestroyAPIView):
    queryset = Classified.objects.all()
    serializer_class = DeleteClassifiedSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, permissions.IsAdminUser]


@method_decorator(cache_page(60*15), name='dispatch')
class CreateClassifiedView(generics.CreateAPIView):
    serializer_class = CreateClassifiedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            return Classified.objects.filter(classified__owner=self.request.user)
        except:
            return None


@method_decorator(cache_page(60*15), name='dispatch')
class CreateClassifiedImageView(generics.CreateAPIView):
    serializer_class = CreateClassifiedImageSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, DraftClassifiedPermission]

    def get_queryset(self):
        try:
            return ClassifiedImage.objects.filter(classified__owner=self.request.user)
        except:
            return None

    def perform_create(self, serializer):
        classified = get_object_or_404(Classified, pk=self.kwargs['pk'])
        images = self.request.FILES
        serializer.save(classified=classified, images=images)


@method_decorator(cache_page(60*15), name='dispatch')
class CreateClassifiedDetailView(generics.CreateAPIView):
    serializer_class = CreateClassifiedDetailSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, DraftClassifiedPermission]

    def get_queryset(self):
        try:
            return ClassifiedDetail.objects.filter(classified__owner=self.request.user)
        except:
            return None

    def perform_create(self, serializer):
        classified = get_object_or_404(Classified, pk=self.kwargs['pk'])
        return serializer.save(classified=classified)


@method_decorator(cache_page(60*15), name='dispatch')
class EditClassifiedView(generics.UpdateAPIView):
    serializer_class = CreateClassifiedSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, PublishedClassifiedPermission]

    def get_queryset(self):
        try:
            return Classified.objects.filter(classified__owner=self.request.user)
        except:
            return None


@method_decorator(cache_page(60*15), name='dispatch')
class EditClassifiedImageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassifiedImageSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, PublishedClassifiedPermission]

    def get_queryset(self):
        try:
            return ClassifiedImage.objects.filter(classified__owner=self.request.user)
        except:
            return None

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(ClassifiedImage, pk=pk)

    def check_object_permissions(self, request, obj):
        if not request.user.has_perm('can_edit_classified', obj.classified):
            raise PermissionDenied()


@method_decorator(cache_page(60*15), name='dispatch')
class EditClassifiedDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateClassifiedDetailSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, PublishedClassifiedPermission]

    def get_queryset(self):
        try:
            return ClassifiedDetail.objects.filter(classified__owner=self.request.user)
        except:
            return None

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(ClassifiedDetail, classified__pk=pk)

    def check_object_permissions(self, request, obj):
        if not request.user.has_perm('can_edit_classified', obj.classified):
            raise PermissionDenied()
