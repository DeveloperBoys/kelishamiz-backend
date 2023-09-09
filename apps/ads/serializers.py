from rest_framework import serializers

from .models import ClassifiedAd


class ClassifiedAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedAd
        fields = '__all__'
