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
        fields = ['id', 'name', 'url']


class AppStoreLinkSerializer(serializers.ModelSerializer):
    appName = serializers.CharField(source='app_name')
    iosUrl = serializers.URLField(source='ios_url')
    androidUrl = serializers.URLField(source='android_url')

    class Meta:
        model = AppStoreLink
        fields = ['id', 'appName', 'iosUrl', 'androidUrl']


class CompanyInfoSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.CharField(source='phone_number')
    socialMedia = SocialMediaSerializer(many=True, source='social_media')
    appLinks = AppStoreLinkSerializer(many=True, source='app_links')
    logoUrl = serializers.URLField(source='logo_url', read_only=True)

    class Meta:
        model = CompanyInfo
        fields = ['id', 'phoneNumber', 'socialMedia',
                  'appLinks', 'logoUrl', 'logo']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method == 'GET':
            data.pop('logo', None)
        elif request and request.method == 'POST' or 'PUT' or 'PATCH' or 'DELETE':
            data.pop('logoUrl', None)

        return data


class BannerSerializer(serializers.ModelSerializer):
    shortDescription = serializers.CharField(source='short_description')
    imageUrl = serializers.URLField(source='image_url', read_only=True)

    class Meta:
        model = Banner
        fields = ['id', 'title', 'shortDescription',
                  'imageUrl', 'image', 'url']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method == 'GET':
            data.pop('image', None)
        elif request and request.method == 'POST' or 'PUT' or 'PATCH' or 'DELETE':
            data.pop('imageUrl', None)

        return data
