from rest_framework import serializers

from .models import ClassifiedLike, ClassifiedView


class ClassifiedLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedLike
        fields = ('id', 'classified', )
        read_only_fields = ('id',)


class ClassifiedViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassifiedView
        fields = ('id', 'classified', 'viewed_at')
        read_only_fields = ('id', 'viewed_at')
