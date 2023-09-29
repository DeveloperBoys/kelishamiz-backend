from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions

from django_filters.rest_framework import DjangoFilterBackend

from apps.permissions.permissions import PublishedClassifiedPermission, ClassifiedOwner, IsAdminOrReadOnly, DraftClassifiedPermission
from .models import Category, Classified, ClassifiedImage, APPROVED
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


class ClassifiedListView(generics.ListAPIView):
    queryset = Classified.objects.filter(status=APPROVED).order_by('-created_at')
    serializer_class = ClassifiedListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_class = ClassifiedFilter
    pagination_class = ClassifiedPagination


class ClassifiedDetailView(generics.ListAPIView):
    queryset = Classified.objects.filter(status=APPROVED)
    serializer_class = ClassifiedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    
    
class DeleteClassifiedView(generics.UpdateAPIView):
    queryset = Classified.objects.all()
    serializer_class = DeleteClassifiedSerializer
    permission_classes = [permissions.IsAuthenticated, ClassifiedOwner, permissions.IsAdminUser]


class CreateClassifiedView(generics.CreateAPIView):
    serializer_class = CreateClassifiedSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateClassifiedImageView(generics.CreateAPIView):
    serializer_class = ClassifiedImageSerializer
    permission_classes = [permissions.IsAuthenticated, ClassifiedOwner, DraftClassifiedPermission]


class CreateClassifiedDetailView(generics.CreateAPIView):
    serializer_class = CreateClassifiedDetailSerializer
    permission_classes = [permissions.IsAuthenticated, ClassifiedOwner, DraftClassifiedPermission]


class EditClassifiedView(generics.UpdateAPIView):
    serializer_class = CreateClassifiedSerializer
    permission_classes = [permissions.IsAuthenticated, ClassifiedOwner, PublishedClassifiedPermission]


class EditClassifiedImageView(generics.UpdateAPIView):
    serializer_class = ClassifiedImageSerializer
    permission_classes = [permissions.IsAuthenticated, ClassifiedOwner, PublishedClassifiedPermission]
    

class EditClassifiedDetailView(generics.UpdateAPIView):
    serializer_class = CreateClassifiedDetailSerializer
    permission_classes = [permissions.IsAuthenticated, ClassifiedOwner, PublishedClassifiedPermission]
    