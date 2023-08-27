from rest_framework import serializers

from .models import ClassifiedLike
from classifieds.serializers import ClassifiedListSerializer


class ClassifiedLikeSerializer(serializers.ModelSerializer):
    classifieds = ClassifiedListSerializer(
        many=True, read_only=True, source='classified')

    class Meta:
        model = ClassifiedLike
        fields = ('classifieds', )

    def to_representation(self, instance):
        if not instance.is_active:
            return {}  # If not active, return an empty dictionary
        return super().to_representation(instance)
