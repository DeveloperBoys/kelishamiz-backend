import os
import shutil
from django.conf import settings

from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, response, pagination


from apps.ads.models import TopClassified
from apps.permissions.permissions import ClassifiedOwnerOrReadOnly, IsAdminOrReadOnly
from .models import Category, Classified, ClassifiedDetail, ClassifiedImage, DynamicField
from .serializers import (
    CategorySerializer,
    ClassifiedListSerializer,
    ClassifiedSerializer,
    ClassifiedImageSerializer
)


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
    queryset = Classified.objects.all()
    serializer_class = ClassifiedListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    http_method_names = ['get', ]


class ClassifiedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classified.objects.all()
    serializer_class = ClassifiedSerializer
    permission_classes = (ClassifiedOwnerOrReadOnly, )


class CombinedClassifiedListView(generics.ListCreateAPIView):
    serializer_class = ClassifiedListSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        top_classified_ids = TopClassified.objects.filter(
            is_active=True).values_list('classified_id', flat=True)

        # top_classifieds = TopClassified.objects.filter(
        #     is_active=True).order_by('classified__created_at')
        top_classifieds = Classified.objects.filter(
            is_active=True, id__in=top_classified_ids).order_by('-created_at')

        regular_classifieds = Classified.objects.filter(is_active=True).exclude(
            id__in=top_classified_ids).order_by('-created_at')

        # serialize with request context
        top_serialized = None
        if top_classifieds.exists():
            top_serialized = ClassifiedListSerializer(
                top_classifieds, many=True, context={'request': request}).data

        regular_serialized = ClassifiedListSerializer(
            regular_classifieds, many=True, context={'request': request})

        data = {
            'top_classifieds': top_serialized,
            'regular_classifieds': regular_serialized.data
        }

        return response.Response(data)
