from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions

from django_filters.rest_framework import DjangoFilterBackend

from apps.permissions.permissions import ClassifiedOwnerOrReadOnly, IsAdminOrReadOnly
from .models import Category, Classified, ClassifiedImage
from .filters import ClassifiedFilter
from .serializers import (
    CategorySerializer,
    ClassifiedListSerializer,
    ClassifiedSerializer,
    ClassifiedImageSerializer
)


class ClassifiedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


class ImageView(generics.ListCreateAPIView):
    queryset = ClassifiedImage.objects.all()
    serializer_class = ClassifiedImageSerializer
    permission_classes = (permissions.IsAuthenticated, )


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


class ClassifiedListView(generics.ListCreateAPIView):
    queryset = Classified.objects.filter(
        is_active=True).order_by('-created_at')
    serializer_class = ClassifiedListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_class = ClassifiedFilter
    pagination_class = ClassifiedPagination
    http_method_names = ['get', ]


class ClassifiedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classified.objects.filter(is_active=True)
    serializer_class = ClassifiedSerializer
    permission_classes = (ClassifiedOwnerOrReadOnly, )


class ClassifiedCreateView(generics.CreateAPIView):
    serializer_class = ClassifiedSerializer
    permission_classes = (permissions.IsAuthenticated)
