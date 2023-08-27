from rest_framework import generics

from .models import ClassifiedLike
from .serializers import ClassifiedLikeSerializer


class GetClassifiedLikeView(generics.ListAPIView):
    queryset = ClassifiedLike.objects.filter(is_active=True)
    serializer_class = ClassifiedLikeSerializer
    http_method_names = ['get']
