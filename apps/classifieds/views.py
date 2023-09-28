from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions

from django_filters.rest_framework import DjangoFilterBackend

from apps.permissions.permissions import ClassifiedOwnerOrReadOnly, ClassifiedOwner, IsAdminOrReadOnly, ClassifiedPermission
from .models import Category, Classified, ClassifiedImage, APPROVED
from .filters import ClassifiedFilter
from .serializers import (
    CategorySerializer,
    ClassifiedListSerializer,
    ClassifiedSerializer,
    ClassifiedImageSerializer,
    CreateClassifiedSerializer,
    CreateClassifiedImageSerializer,
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


class ClassifiedListView(generics.ListCreateAPIView):
    queryset = Classified.objects.filter(status=APPROVED).order_by('-created_at')
    serializer_class = ClassifiedListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    filterset_class = ClassifiedFilter
    pagination_class = ClassifiedPagination
    http_method_names = ['get', ]


class ClassifiedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classified.objects.filter(status=APPROVED)
    serializer_class = ClassifiedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ClassifiedOwnerOrReadOnly, ]
    
    # def get_queryset(self):
    #     # Check if the request method is GET and the user is authenticated.
    #     if self.request.method == 'GET' and self.request.user.is_authenticated:
    #         # Return approved classifieds for GET requests from authenticated users.
    #         return Classified.objects.filter(status=APPROVED)
        
    #     # For other methods (e.g., PUT, DELETE) or unauthenticated users, return all classifieds.
    #     return Classified.objects.all()


class CreateClassifiedView(generics.CreateAPIView):
    serializer_class = CreateClassifiedSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateClassifiedImageView(generics.CreateAPIView):
    serializer_class = CreateClassifiedImageSerializer
    permission_classes = [ClassifiedOwner, ClassifiedPermission]


class CreateClassifiedDetailView(generics.CreateAPIView):
    serializer_class = CreateClassifiedDetailSerializer
    permission_classes = [ClassifiedOwner, ClassifiedPermission]
