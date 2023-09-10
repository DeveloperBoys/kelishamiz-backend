from rest_framework import serializers

from .models import (
    Banner,
    SocialMedia,
    CompanyInfo,
    AppStoreLink
)


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['name', 'url']


class AppStoreLinkSerializer(serializers.ModelSerializer):
    appName = serializers.CharField(source='app_name')
    iosUrl = serializers.URLField(source='ios_url')
    androidUrl = serializers.URLField(source='android_url')

    class Meta:
        model = AppStoreLink
        fields = ['appName', 'iosUrl', 'androidUrl']


class CompanyInfoSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.CharField(source='phone_number')
    socialMedia = SocialMediaSerializer(many=True)
    appLinks = AppStoreLinkSerializer()
    logoUrl = serializers.URLField(source='logo_url')

    class Meta:
        model = CompanyInfo
        fields = ['phoneNumber', 'socialMedia', 'appLinks', 'logoUrl']


class BannerSerializer(serializers.ModelSerializer):
    shortDescription = serializers.CharField(source='short_description')
    imageUrl = serializers.URLField(source='image_url')

    class Meta:
        model = Banner
        fields = ['title', 'shortDescription', 'imageUrl', 'url']
