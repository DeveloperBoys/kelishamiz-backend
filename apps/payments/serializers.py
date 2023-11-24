from rest_framework import serializers

from .models import CustomOrder, UserBalance


class CustomOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomOrder
        fields = '__all__'


class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = '__all__'
