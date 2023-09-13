from rest_framework import generics, permissions, response

from apps.ads.models import TopClassified
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


class CombinedClassifiedListView(generics.ListCreateAPIView):

    serializer_class = ClassifiedListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        top_classified_ids = TopClassified.objects.filter(
            is_active=True).values_list('classified_id', flat=True)

        top_classifieds = TopClassified.objects.filter(is_active=True)

        regular_classifieds = Classified.objects.filter(
            is_active=True).exclude(id__in=top_classified_ids)

        data = {
            'top_classifieds': ClassifiedListSerializer(top_classifieds, many=True).data,
            'regular_classifieds': ClassifiedListSerializer(regular_classifieds, many=True).data
        }

        return response.Response(data)
