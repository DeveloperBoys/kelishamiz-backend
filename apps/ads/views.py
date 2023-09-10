from rest_framework import generics, permissions

from apps.permissions.permissions import IsAdminOrReadOnly
from .models import ClassifiedAd, AdType, AdTypeAttribute
from .serializers import ClassifiedAdSerializer, AdTypeSerializer, AdTypeAttributeSerializer


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
