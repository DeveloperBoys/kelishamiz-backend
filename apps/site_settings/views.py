from rest_framework import generics

from apps.permissions.permissions import IsAdminOrReadOnly

from .models import (
    Banner,
    Company,
    AppStoreLink,
    SocialMediaProfile
)
from .serializers import (
    BannerSerializer,
    CompanySerializer,
    AppStoreLinkSerializer,
    SocialMediaProfileSerializer
)


class AppStoreLinkListCreateView(generics.ListCreateAPIView):
    queryset = AppStoreLink.objects.all()
    serializer_class = AppStoreLinkSerializer
    permission_classes = [IsAdminOrReadOnly]


class AppStoreLinkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppStoreLink.objects.all()
    serializer_class = AppStoreLinkSerializer
    permission_classes = [IsAdminOrReadOnly]


class SocialMediaProfileListCreateView(generics.ListCreateAPIView):
    queryset = SocialMediaProfile.objects.all()
    serializer_class = SocialMediaProfileSerializer
    permission_classes = [IsAdminOrReadOnly]


class SocialMediaProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialMediaProfile.objects.all()
    serializer_class = SocialMediaProfileSerializer
    permission_classes = [IsAdminOrReadOnly]


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]


class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]


class BannerListCreateView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]


class BannerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]
