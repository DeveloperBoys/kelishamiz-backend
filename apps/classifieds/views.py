import os
import shutil
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, response, pagination, status

from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method, swagger_auto_schema

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
    serializer_class = ClassifiedSerializer
    permission_classes = (permissions.IsAuthenticated)

    def perform_create(self, serializer):
        classified = serializer.save()
        for image_data in serializer.validated_data.get('images', []):

            image = self.handle_image(image_data, classified)
            image.save()

        return classified

    def handle_image(self, image_data, classified):

        if not image_data.get('imageUrl'):
            raise ValidationError('Image URL required')

        image_path = image_data['imageUrl']

        if not os.path.exists(image_path):
            raise ValidationError('Image not found')

        image_name = os.path.basename(image_path)

        shutil.copy(
            image_path,
            os.path.join(settings.MEDIA_ROOT, 'classifieds', image_name)
        )

        return ClassifiedImage(
            classified=classified,
            image=f'classifieds/{image_name}'
        )


class CombinedClassifiedListView(generics.ListCreateAPIView):
    serializer_class = ClassifiedListSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        top_classified_ids = TopClassified.objects.filter(
            is_active=True).values_list('classified_id', flat=True)

        top_classifieds = TopClassified.objects.filter(
            is_active=True).order_by('classified__created_at')

        regular_classifieds = Classified.objects.filter(is_active=True).exclude(
            id__in=top_classified_ids).order_by('-created_at')

        # serialize with request context
        top_serialized = ClassifiedListSerializer(
            top_classifieds, many=True, context={'request': request})

        regular_serialized = ClassifiedListSerializer(
            regular_classifieds, many=True, context={'request': request})

        data = {
            'top_classifieds': top_serialized.data,
            'regular_classifieds': regular_serialized.data
        }

        return response.Response(data)
