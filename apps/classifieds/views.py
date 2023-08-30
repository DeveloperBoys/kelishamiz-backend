from rest_framework import generics, permissions

from .models import Category, DynamicField, Classified, ClassifiedDetail, ClassifiedImage
from .serializers import (
    DynamicFieldSerializer,
    CategorySerializer,
    ClassifiedDetailSerializer,
    ClassifiedImageSerializer,
    ClassifiedListSerializer,
    ClassifiedSerializer,
    ClassifiedCreateSerializer,
)


class ClassifiedOwnerPermission(permissions.BasePermission):
    """
    Custom permission to allow only classified owners to perform CRUD operations.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class DynamicFieldListView(generics.ListCreateAPIView):
    queryset = DynamicField.objects.all()
    serializer_class = DynamicFieldSerializer
    permission_classes = (ClassifiedOwnerPermission, )


class DynamicFieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DynamicField.objects.all()
    serializer_class = DynamicFieldSerializer
    permission_classes = (ClassifiedOwnerPermission, )


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUser, )


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUser, )


class ClassifiedDetailListView(generics.ListCreateAPIView):
    queryset = ClassifiedDetail.objects.all()
    serializer_class = ClassifiedDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class ClassifiedDetailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassifiedDetail.objects.all()
    serializer_class = ClassifiedDetailSerializer
    permission_classes = (ClassifiedOwnerPermission, )


class ClassifiedImageView(generics.ListCreateAPIView):
    queryset = ClassifiedImage.objects.all()
    serializer_class = ClassifiedImageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class ClassifiedImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassifiedImage.objects.all()
    serializer_class = ClassifiedImageSerializer
    permission_classes = (ClassifiedOwnerPermission, )


class ClassifiedListView(generics.ListCreateAPIView):
    queryset = Classified.objects.all()
    serializer_class = ClassifiedListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class ClassifiedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classified.objects.all()
    serializer_class = ClassifiedSerializer
    permission_classes = (ClassifiedOwnerPermission, )


class ClassifiedCreateView(generics.CreateAPIView):
    queryset = Classified.objects.all()
    serializer_class = ClassifiedCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )
