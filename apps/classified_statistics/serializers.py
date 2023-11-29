from rest_framework import serializers

from .models import ClassifiedLike


class ClassifiedLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedLike
        fields = ('id', 'classified', )

    def to_representation(self, instance):
        if not instance.is_active:
            return {}
        return super().to_representation(instance)
