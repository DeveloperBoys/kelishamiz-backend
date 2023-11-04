from rest_framework import serializers

from .models import (
    Banner,
    Company,
    AppStoreLink,
    SocialMediaProfile
)


class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method in ['POST', 'PUT', 'PATCH']:
            for field in self.read_only_fields:
                data.pop(field, None)

        return data


class SocialMediaProfileSerializer(BaseSerializer):
    iconUrl = serializers.URLField(source='icon_url', read_only=True)

    class Meta:
        model = SocialMediaProfile
        fields = ['id', 'platform', 'url', 'icon', 'iconUrl']
        read_only_fields = ['id', 'iconUrl']


class AppStoreLinkSerializer(BaseSerializer):
    logoUrl = serializers.URLField(source='logo_url', read_only=True)

    class Meta:
        model = AppStoreLink
        fields = ['id', 'platform', 'url', 'logo', 'logoUrl']
        read_only_fields = ['id', 'logoUrl']


class CompanySerializer(BaseSerializer):
    appLinks = AppStoreLinkSerializer(many=True, read_only=True)
    socialMediaProfiles = SocialMediaProfileSerializer(
        many=True, read_only=True)
    logoUrl = serializers.URLField(source='logo_url', read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'phone', 'website', 'logo', 'logoUrl',
                  'socialMediaProfiles', 'appLinks']
        read_only_fields = ['id', 'logoUrl', 'appLinks', 'socialMediaProfiles']


class BannerSerializer(BaseSerializer):
    imageUrl = serializers.URLField(source='image_url', read_only=True)

    class Meta:
        model = Banner
        fields = ['id', 'title', 'short_description',
                  'image', 'imageUrl', 'url']
        read_only_fields = ['id', 'imageUrl']
