from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

from .models import ClassifiedLike
from .serializers import ClassifiedLikeSerializer


class CreateClassifiedLikeView(generics.CreateAPIView):
    queryset = ClassifiedLike.objects.all()
    serializer_class = ClassifiedLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_active=True)


class GetClassifiedLikeView(generics.ListAPIView):
    serializer_class = ClassifiedLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return ClassifiedLike.objects.filter(user=user, is_active=True)


class DeleteClassifiedLikeView(generics.DestroyAPIView):
    queryset = ClassifiedLike.objects.filter(is_active=True)
    serializer_class = ClassifiedLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
