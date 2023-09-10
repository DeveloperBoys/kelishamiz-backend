from rest_framework import serializers

from .models import ClassifiedAd, AdTypeAttribute, AdType


class AdTypeAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdTypeAttribute
        fields = ['name']


class AdTypeSerializer(serializers.ModelSerializer):
    validityPeriod = serializers.CharField(source='validity_period')
    attributes = AdTypeAttributeSerializer(many=True)  # Fix the typo here

    class Meta:
        model = AdType
        fields = ['name', 'icon', 'price',
                  'short_description' 'validityPeriod', 'attributes']


class ClassifiedAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedAd
        fields = '__all__'
