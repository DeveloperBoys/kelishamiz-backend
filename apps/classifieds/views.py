from rest_framework import generics, permissions

from apps.permissions.permissions import ClassifiedOwnerOrReadOnly, IsAdminOrReadOnly
from .models import Category, Classified
from .serializers import (
    CategorySerializer,
    ClassifiedListSerializer,
    ClassifiedSerializer,
    ClassifiedCreateSerializer,
)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


class ClassifiedListView(generics.ListCreateAPIView):
    queryset = Classified.objects.all()
    serializer_class = ClassifiedListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    http_method_names = ['get', ]


class ClassifiedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classified.objects.all()
    serializer_class = ClassifiedSerializer
    permission_classes = (ClassifiedOwnerOrReadOnly, )


class ClassifiedCreateView(generics.CreateAPIView):
    queryset = Classified.objects.all()
    serializer_class = ClassifiedCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )
