import memcache
import threading

from PIL import Image
from io import BytesIO

from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import generics, permissions
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
    DeleteClassifiedSerializer,
    ClassifiedCreateSerializer,
    CreateClassifiedDetailSerializer
)


memcache_client = memcache.Client(['127.0.0.1:11211'])


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
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


@method_decorator(cache_page(60*15), name='dispatch')
class ClassifiedDetailView(generics.RetrieveAPIView):
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
    serializer_class = ClassifiedCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            return Classified.objects.filter(classified=self.kwargs['pk'])
        except:
            return None

    def post(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        classified = serializer.save()

        uploaded_files = [SimpleUploadedFile(f.name, f.read())
                          for f in request.FILES.getlist('images')]

        batch = []

        def upload_file(uploaded_file):
            if uploaded_file.size > 4*1024*1024:
                output = BytesIO()
                Image.open(uploaded_file).convert('RGB').save(
                    output, format='JPEG', optimize=True, quality=85)
                output.seek(0)
                uploaded_file = SimpleUploadedFile(
                    uploaded_file.name, output.read())

            image = ClassifiedImage(classified=classified, image=uploaded_file)
            batch.append(image)

            from django.db import connection
            connection.close()

        threads = []
        for uploaded_file in uploaded_files:
            thread = threading.Thread(target=upload_file, args=[uploaded_file])
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        ClassifiedImage.objects.bulk_create(batch)

        return Response(status=204)


@method_decorator(cache_page(60*15), name='dispatch')
class EditClassifiedView(generics.UpdateAPIView):
    serializer_class = ClassifiedCreateSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, PublishedClassifiedPermission]

    def get_queryset(self):
        try:
            return Classified.objects.filter(classified=self.kwargs['pk'])
        except:
            return None


@method_decorator(cache_page(60*15), name='dispatch')
class EditClassifiedImageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassifiedImageSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, PublishedClassifiedPermission]

    def get_queryset(self):
        try:
            return ClassifiedImage.objects.filter(classified=self.kwargs['pk'])
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
            return ClassifiedDetail.objects.filter(classified=self.kwargs['pk'])
        except:
            return None

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(ClassifiedDetail, classified__pk=pk)

    def check_object_permissions(self, request, obj):
        if not request.user.has_perm('can_edit_classified', obj.classified):
            raise PermissionDenied()
