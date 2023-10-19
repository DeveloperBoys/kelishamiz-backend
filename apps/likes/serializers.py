from rest_framework import serializers

from .models import ClassifiedLike
from apps.classifieds.serializers import ClassifiedListSerializer


class ClassifiedLikeSerializer(serializers.ModelSerializer):
    classifieds = ClassifiedListSerializer(
        many=True, source='classified')

    class Meta:
        model = ClassifiedLike
        fields = ('id', 'classifieds', )

    def to_representation(self, instance):
        if not instance.is_active:
            return {}
        return super().to_representation(instance)
