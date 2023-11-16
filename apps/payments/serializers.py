from rest_framework import serializers

from .models import CustomOrder


class CustomOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrder
        fields = '__all__'
