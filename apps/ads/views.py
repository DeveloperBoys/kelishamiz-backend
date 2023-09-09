from rest_framework import generics, permissions

from .models import ClassifiedAd
from .serializers import ClassifiedAdSerializer


class ClassifiedAdListCreateView(generics.ListCreateAPIView):
    queryset = ClassifiedAd.objects.all()
    serializer_class = ClassifiedAdSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassifiedAdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassifiedAd.objects.all()
    serializer_class = ClassifiedAdSerializer
    permission_classes = [permissions.IsAuthenticated]
