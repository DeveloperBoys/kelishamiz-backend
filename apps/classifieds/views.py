from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.filters import SearchFilter
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema

from django_filters.rest_framework import DjangoFilterBackend

from apps.permissions.permissions import PublishedClassifiedPermission, ClassifiedOwner, IsAdminOrReadOnly, DraftClassifiedPermission
from .models import Category, Classified, ClassifiedImage, ClassifiedDetail, APPROVED
from apps.user_searches.models import SearchQuery
from .filters import ClassifiedFilter
from .serializers import (
    CategorySerializer,
    ClassifiedListSerializer,
    ClassifiedSerializer,
    ClassifiedImageSerializer,
    CreateClassifiedSerializer,
    DeleteClassifiedSerializer,
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

    @method_decorator(cache_page(60*15))
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
class DeleteClassifiedView(generics.UpdateAPIView):
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
    serializer_class = ClassifiedImageSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, DraftClassifiedPermission]

    def get_queryset(self):
        try:
            return ClassifiedImage.objects.filter(classified__owner=self.request.user)
        except:
            return None


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


@swagger_auto_schema(exclude=['get_queryset'])
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
class EditClassifiedImageView(generics.UpdateAPIView):
    serializer_class = ClassifiedImageSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, PublishedClassifiedPermission]

    def get_queryset(self):
        try:
            return ClassifiedImage.objects.filter(classified__owner=self.request.user)
        except:
            return None


@method_decorator(cache_page(60*15), name='dispatch')
class EditClassifiedDetailView(generics.UpdateAPIView):
    serializer_class = CreateClassifiedDetailSerializer
    permission_classes = [permissions.IsAuthenticated,
                          ClassifiedOwner, PublishedClassifiedPermission]

    def get_queryset(self):
        try:
            return ClassifiedDetail.objects.filter(classified__owner=self.request.user)
        except:
            return None
