from rest_framework import serializers

from .models import (
    Banner,
    Company,
    Locations,
    AppStoreLink,
    SocialMediaProfile
)


class SocialMediaProfileSerializer(serializers.ModelSerializer):
    iconUrl = serializers.URLField(source='icon_url', read_only=True)

    class Meta:
        model = SocialMediaProfile
        fields = ['id', 'company', 'platform', 'url', 'icon', 'iconUrl']
        read_only_fields = ['id',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method != 'GET':
            data.pop('iconUrl', None)
        else:
            data.pop('icon', None)

        return data


class AppStoreLinkSerializer(serializers.ModelSerializer):
    logoUrl = serializers.URLField(source='logo_url', read_only=True)

    class Meta:
        model = AppStoreLink
        fields = ['id', 'company', 'platform', 'url', 'logo', 'logoUrl']
        read_only_fields = ['id',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method != 'GET':
            data.pop('logoUrl', None)
        else:
            data.pop('logo', None)

        return data


class CompanySerializer(serializers.ModelSerializer):
    appLinks = serializers.SerializerMethodField(read_only=True)
    logoUrl = serializers.URLField(source='logo_url', read_only=True)
    socialMediaProfiles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'phone', 'website', 'logo', 'logoUrl',
                  'socialMediaProfiles', 'appLinks']
        read_only_fields = ['id',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method != 'GET':
            data.pop('logoUrl', None)
            data.pop('appLinks', None)
            data.pop('socialMediaProfiles', None)
        else:
            data.pop('logo', None)

        return data

    def get_appLinks(self, obj):
        app_links = AppStoreLink.objects.filter(company=obj)
        if app_links.exists():
            return AppStoreLinkSerializer(app_links, many=True).data
        return None

    def get_socialMediaProfiles(self, obj):
        social_media = SocialMediaProfile.objects.filter(company=obj)
        if social_media.exists():
            return SocialMediaProfileSerializer(social_media, many=True).data
        return None


class BannerSerializer(serializers.ModelSerializer):
    imageUrl = serializers.URLField(source='image_url', read_only=True)

    class Meta:
        model = Banner
        fields = ['id', 'title', 'short_description',
                  'image', 'imageUrl', 'url']
        read_only_fields = ['id',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method != 'GET':
            data.pop('imageUrl', None)
        else:
            data.pop('image', None)

        return data


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Locations
        fields = ['id', 'name', 'latitude', 'longitude']
        read_only_fields = ['id',]
