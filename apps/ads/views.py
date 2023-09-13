from rest_framework import generics, permissions

from apps.permissions.permissions import IsAdminOrReadOnly
from .models import ClassifiedAd, AdType, AdTypeAttribute, TopClassified
from .serializers import ClassifiedAdSerializer, AdTypeSerializer, AdTypeAttributeSerializer
from apps.classifieds.serializers import ClassifiedListSerializer


class AdTypeAttributeListCreateView(generics.ListCreateAPIView):
    queryset = AdTypeAttribute.objects.all()
    serializer_class = AdTypeAttributeSerializer
    permission_classes = [IsAdminOrReadOnly]


class AdTypeAttributeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdTypeAttribute.objects.all()
    serializer_class = AdTypeAttributeSerializer
    permission_classes = [IsAdminOrReadOnly]


class AdTypeListCreateView(generics.ListCreateAPIView):
    queryset = AdType.objects.all()
    serializer_class = AdTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class AdTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdType.objects.all()
    serializer_class = AdTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class ClassifiedAdListCreateView(generics.ListCreateAPIView):
    queryset = ClassifiedAd.objects.all()
    serializer_class = ClassifiedAdSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassifiedAdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassifiedAd.objects.all()
    serializer_class = ClassifiedAdSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']


class TopClassifiedListView(generics.ListView):
    queryset = TopClassified.objects.filter(is_active=True)
    serializer_class = ClassifiedListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
