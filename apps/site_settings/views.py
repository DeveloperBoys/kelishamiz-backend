from rest_framework import generics

from apps.permissions.permissions import IsAdminOrReadOnly

from .models import (
    Banner,
    SocialMedia,
    CompanyInfo,
    AppStoreLink,
)

from .serializers import (
    BannerSerializer,
    SocialMediaSerializer,
    CompanyInfoSerializer,
    AppStoreLinkSerializer,
)


class SocialMediaListCreateView(generics.ListCreateAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = [IsAdminOrReadOnly]


class SocialMediaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = [IsAdminOrReadOnly]


class AppStoreLinkListCreateView(generics.ListCreateAPIView):
    queryset = AppStoreLink.objects.all()
    serializer_class = AppStoreLinkSerializer
    permission_classes = [IsAdminOrReadOnly]


class AppStoreLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppStoreLink.objects.all()
    serializer_class = AppStoreLinkSerializer
    permission_classes = [IsAdminOrReadOnly]


class CompanyInfoListCreateView(generics.ListCreateAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [IsAdminOrReadOnly]


class CompanyInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [IsAdminOrReadOnly]


class BannerListCreateView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]


class BannerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]
