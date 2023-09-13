from rest_framework import serializers

from .models import ClassifiedAd, AdTypeAttribute, AdType


class AdTypeAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdTypeAttribute
        fields = ['id', 'name']


class AdTypeSerializer(serializers.ModelSerializer):
    validityPeriod = serializers.CharField(source='validity_period')
    shortDescription = serializers.CharField(source='short_description')
    attributes = AdTypeAttributeSerializer(many=True)

    class Meta:
        model = AdType
        fields = ['id', 'name', 'icon', 'price',
                  'shortDescription', 'validityPeriod', 'attributes']

    def create(self, validated_data):
        attributes_data = validated_data.pop('attributes')
        ad_type = AdType.objects.create(**validated_data)
        for attribute_data in attributes_data:
            AdTypeAttribute.objects.create(ad_type=ad_type, **attribute_data)
        return ad_type


class ClassifiedAdSerializer(serializers.ModelSerializer):
    adType = serializers.CharField(source="ad_type.name")
    isActive = serializers.BooleanField(source="is_active")
    startedDate = serializers.DateTimeField(source="started_date")
    endedDate = serializers.DateTimeField(source="ended_date")

    class Meta:
        model = ClassifiedAd
        fields = ['id', 'adType', 'isActive', 'startedDate', 'endedDate']
