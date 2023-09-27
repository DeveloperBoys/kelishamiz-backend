import json
from rest_framework import serializers

from .models import (
    Category,
    Classified,
    DynamicField,
    ClassifiedImage,
    ClassifiedDetail
)


class ChildCategorySerializer(serializers.ModelSerializer):
    iconUrl = serializers.URLField(source="icon_url")

    class Meta:
        model = Category
        fields = ('id', 'name', 'iconUrl')


class CategorySerializer(serializers.ModelSerializer):
    iconUrl = serializers.FileField(source="icon")
    childs = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'iconUrl', 'childs')
        read_only_fields = ('icon_url',)

    def get_childs(self, obj):
        childs = obj.children.all()
        return ChildCategorySerializer(childs, many=True).data if childs.exists() else None


class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicField
        fields = ('key', 'value')
        
        
        
class ClassifiedImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.URLField(source="image_url")

    class Meta:
        model = ClassifiedImage
        fields = ('id', 'classified', 'image', 'imageUrl',)
        read_only_field = ('id', 'imageUrl')


class ClassifiedDetailSerializer(serializers.ModelSerializer):
    currencyType = serializers.CharField(
        source='currency_type', required=False)
    dynamicFields = serializers.SerializerMethodField(source='dynamic_fields')
    images = serializers.SerializerMethodField()

    class Meta:
        model = ClassifiedDetail
        fields = ('currencyType', 'price', 'description', 'dynamicFields', 'images')
        
    def get_dynamicFields(self, obj):
        dynamic_fields = obj.dynamic_fields
        if dynamic_fields.exists():
            return DynamicFieldSerializer(dynamic_fields, many=True).data
        return None
        
    def get_images(self, obj):
        images = ClassifiedImage.objects.filter(classified=obj.classified)
        if images.exists():
            return ClassifiedImageSerializer(images, many=True).data
        return None


class ClassifiedListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    imageUrl = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at')
    isLiked = serializers.BooleanField(source='is_liked')

    class Meta:
        model = Classified
        fields = ('id', 'category', 'owner', 'title', 'imageUrl',
                  'price', 'isLiked', 'createdAt')
        read_only_fields = ('id', 'imageUrl', 'price')

    def get_price(self, obj):
        classified_detail = ClassifiedDetail.objects.filter(
            classified=obj).first()
        return classified_detail.price if classified_detail else None

    def get_imageUrl(self, obj):
        classified_image = ClassifiedImage.objects.filter(
            classified=obj).first()
        return classified_image.image_url if classified_image else None


class ClassifiedSerializer(serializers.ModelSerializer):
    detail = ClassifiedDetailSerializer(source='classifieddetail')
    category = serializers.CharField(source='category.name')
    isLiked = serializers.BooleanField(source='is_liked')
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Classified
        fields = ('id', 'title', 'category', 'detail', 'isLiked', 'createdAt')
        read_only_fields = ('id', 'createdAt')
