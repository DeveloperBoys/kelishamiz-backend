from rest_framework import generics

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


class DynamicFieldListView(generics.ListCreateAPIView):
    queryset = DynamicField.objects.all()
    serializer_class = DynamicFieldSerializer


class DynamicFieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DynamicField.objects.all()
    serializer_class = DynamicFieldSerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ClassifiedDetailListView(generics.ListCreateAPIView):
    queryset = ClassifiedDetail.objects.all()
    serializer_class = ClassifiedDetailSerializer


class ClassifiedDetailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassifiedDetail.objects.all()
    serializer_class = ClassifiedDetailSerializer


class ClassifiedImageView(generics.ListCreateAPIView):
    queryset = ClassifiedImage.objects.all()
    serializer_class = ClassifiedImageSerializer


class ClassifiedImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassifiedImage.objects.all()
    serializer_class = ClassifiedImageSerializer


class ClassifiedListView(generics.ListCreateAPIView):
    queryset = Classified.objects.all()
    serializer_class = ClassifiedListSerializer


class ClassifiedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classified.objects.all()
    serializer_class = ClassifiedSerializer


class ClassifiedCreateView(generics.CreateAPIView):
    queryset = Classified.objects.all()
    serializer_class = ClassifiedCreateSerializer
