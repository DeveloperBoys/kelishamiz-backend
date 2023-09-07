from rest_framework import generics, permissions

from .models import (
    AdType,
    Banner,
    SocialMedia,
    CompanyInfo,
    AppStoreLink,
    AdTypeAttribute,
)

from .serializers import (
    AdTypeSerializer,
    BannerSerializer,
    SocialMediaSerializer,
    CompanyInfoSerializer,
    AppStoreLinkSerializer,
    AdTypeAttributeSerializer,
)


class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET requests for all users
        if request.method == 'GET':
            return True
        # Allow other requests only for admin users
        return request.user and request.user.is_staff


class SocialMediaListCreateView(generics.ListCreateAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = [AdminOnlyPermission]


class SocialMediaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = [AdminOnlyPermission]


class AppStoreLinkListCreateView(generics.ListCreateAPIView):
    queryset = AppStoreLink.objects.all()
    serializer_class = AppStoreLinkSerializer
    permission_classes = [AdminOnlyPermission]


class AppStoreLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppStoreLink.objects.all()
    serializer_class = AppStoreLinkSerializer
    permission_classes = [AdminOnlyPermission]


class CompanyInfoListCreateView(generics.ListCreateAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [AdminOnlyPermission]


class CompanyInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [AdminOnlyPermission]


class BannerListCreateView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [AdminOnlyPermission]


class BannerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [AdminOnlyPermission]


class AdTypeAttributeListCreateView(generics.ListCreateAPIView):
    queryset = AdTypeAttribute.objects.all()
    serializer_class = AdTypeAttributeSerializer
    permission_classes = [AdminOnlyPermission]


class AdTypeAttributeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdTypeAttribute.objects.all()
    serializer_class = AdTypeAttributeSerializer
    permission_classes = [AdminOnlyPermission]


class AdTypeListCreateView(generics.ListCreateAPIView):
    queryset = AdType.objects.all()
    serializer_class = AdTypeSerializer
    permission_classes = [AdminOnlyPermission]


class AdTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdType.objects.all()
    serializer_class = AdTypeSerializer
    permission_classes = [AdminOnlyPermission]
