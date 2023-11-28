from rest_framework import generics, permissions

from .models import Ad, AdClassified
from apps.permissions.permissions import IsAdminOrReadOnly
from .serializers import AdSerializer, AdClassifiedSerializer, CreateAdClassifiedSerializer


class AdView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAdminOrReadOnly]


class EditAdView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAdminOrReadOnly]


class AdClassifiedView(generics.ListCreateAPIView):
    serializer_class = CreateAdClassifiedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return AdClassified.objects.filter(classified__owner=self.request.user)
        return None


class EditAdClassifiedView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateAdClassifiedSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return AdClassified.objects.filter(classified__owner=self.request.user)
        return None
