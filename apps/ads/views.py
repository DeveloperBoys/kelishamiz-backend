from rest_framework import generics
from .models import Category, DynamicField, Ad, AdDetail, AdImage
from .serializers import (
    DynamicFieldSerializer,
    CategorySerializer,
    AdDetailSerializer,
    AdImageSerializer,
    AdListSerializer,
    AdSerializer,
    AdCreateSerializer,
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


class AdDetailListView(generics.ListCreateAPIView):
    queryset = AdDetail.objects.all()
    serializer_class = AdDetailSerializer


class AdDetailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdDetail.objects.all()
    serializer_class = AdDetailSerializer


class AdImageView(generics.ListCreateAPIView):
    queryset = AdImage.objects.all()
    serializer_class = AdImageSerializer


class AdImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdImage.objects.all()
    serializer_class = AdImageSerializer


class AdListView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer


class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
