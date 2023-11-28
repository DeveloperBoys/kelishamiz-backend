from rest_framework import serializers

from .models import Ad, AdClassified


class AdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = '__all__'


class CreateAdClassifiedSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdClassified
        fields = ['ad', 'classified', 'start_date']


class AdClassifiedSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdClassified
        fields = ['ad', 'classified', 'start_date', 'end_date']
