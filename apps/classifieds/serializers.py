from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import (
    DRAFT,
    PENDING,
    DELETED,
    Category,
    Classified,
    DynamicField,
    ClassifiedImage,
    ClassifiedDetail,
)


class ChildCategorySerializer(serializers.ModelSerializer):
    iconUrl = serializers.URLField(source="icon_url", read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'iconUrl')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    iconUrl = serializers.URLField(source="icon_url", read_only=True)
    childs = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'icon', 'iconUrl', 'childs')
        read_only_fields = ('id',)

    def get_childs(self, obj):
        childs = obj.children.all()
        return ChildCategorySerializer(childs, many=True).data if childs.exists() else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method != 'GET':
            data.pop('iconUrl', None)
        else:
            data.pop('icon', None)
            data.pop('parent', None)

        return data


class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicField
        fields = ('id', 'key', 'value')
        read_only_fields = ('id', )


class ClassifiedImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.URLField(source="image_url", read_only=True)

    class Meta:
        model = ClassifiedImage
        fields = ('id', 'image', 'imageUrl',)
        read_only_fields = ('id',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        print(request.method)
        if request and request.method != 'GET':
            data.pop('imageUrl', None)
        else:
            data.pop('image', None)

        return data

    def validate(self, data):
        if not self.instance:
            classified = data['classified']
            if classified.status != DRAFT:
                raise serializers.ValidationError(
                    'Classified image must be in draft status')

        return data

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance


class ClassifiedDetailSerializer(serializers.ModelSerializer):
    currencyType = serializers.CharField(source='currency_type')
    dynamicFields = serializers.SerializerMethodField(source='dynamic_fields')
    images = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = ClassifiedDetail
        fields = ('currencyType', 'price', 'description',
                  'dynamicFields', 'location', 'images')

    def get_dynamicFields(self, obj):
        dynamic_fields = DynamicField.objects.filter(classified_detail=obj)
        if dynamic_fields.exists():
            return DynamicFieldSerializer(dynamic_fields, many=True).data
        return None

    def get_location(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            return obj.location.name
        return obj.location.pk

    def get_images(self, obj):
        images = ClassifiedImage.objects.filter(classified=obj.classified)
        if images.exists():
            request = self.context.get('request')
            return ClassifiedImageSerializer(images, many=True, context={'request': request}).data
        return None


class ClassifiedListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    isLiked = serializers.BooleanField(source='is_liked')
    category = serializers.SerializerMethodField()

    class Meta:
        model = Classified
        fields = ('id', 'category', 'owner', 'title', 'images',
                  'price', 'isLiked', 'createdAt')
        read_only_fields = ('id',)

    def get_price(self, obj):
        classified_detail = ClassifiedDetail.objects.filter(
            classified=obj).first()
        return classified_detail.price if classified_detail else None

    def get_category(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            return obj.category.name
        return obj.category.pk

    def get_images(self, obj):
        images = ClassifiedImage.objects.filter(classified=obj)
        if images.exists():
            request = self.context.get('request')
            return ClassifiedImageSerializer(images, many=True, context={'request': request}).data
        return None


class ClassifiedSerializer(serializers.ModelSerializer):
    detail = ClassifiedDetailSerializer()
    isLiked = serializers.BooleanField(source='is_liked')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Classified
        fields = ('id', 'title', 'category', 'detail', 'isLiked', 'createdAt')
        read_only_fields = ('id',)

    def get_category(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            return obj.category.name
        return obj.category.pk

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.category.pk = validated_data.get(
            'category', instance.category.pk)
        instance.save()

        detail_data = validated_data.get('detail', {})
        detail_serializer = ClassifiedDetailSerializer(
            instance=instance.classifieddetail, data=detail_data, partial=True
        )
        if detail_serializer.is_valid():
            detail_serializer.save()

        return instance


class DeleteClassifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classified
        fields = ('id',)

    def update(self, instance, validated_data):
        instance.status = DELETED
        instance.save()
        return instance


class CreateClassifiedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classified
        fields = ('id', 'category', 'title')
        read_only_fields = ('id',)

    def create(self, validated_data):
        classified = Classified.objects.create(
            owner=self.context['request'].user,
            status=DRAFT,
            **validated_data
        )
        return classified

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.category.pk = validated_data.get(
            'category', instance.category.pk)
        instance.save()
        return instance


class CreateClassifiedDetailSerializer(serializers.ModelSerializer):
    dynamicFields = DynamicFieldSerializer(many=True, write_only=True)

    class Meta:
        model = ClassifiedDetail
        fields = ('id', 'classified', 'currency_type', 'price',
                  'is_negotiable', 'description', 'location', 'dynamicFields')
        read_only_fields = ('id', 'classified')

    def create(self, validated_data):
        dynamic_fields_data = validated_data.pop('dynamicFields')
        classified = get_object_or_404(
            Classified, pk=validated_data['classified'])
        classified_detail = ClassifiedDetail.objects.create(**validated_data)

        for dynamic_field_data in dynamic_fields_data:
            DynamicField.objects.create(
                classified_detail=classified_detail, **dynamic_field_data)

        classified.status = PENDING
        classified.save()

        return classified_detail

    def update(self, instance, validated_data):
        instance.currency_type = validated_data.get(
            'currency_type', instance.currency_type)
        instance.price = validated_data.get('price', instance.price)
        instance.is_negotiable = validated_data.get(
            'is_negotiable', instance.is_negotiable)
        instance.description = validated_data.get(
            'description', instance.description)

        dynamic_fields = validated_data.get('dynamicFields')
        if dynamic_fields:
            instance.dynamicfield_set.all().delete()
            for dynamic_field in dynamic_fields:
                DynamicField.objects.create(
                    classified_detail=instance,
                    **dynamic_field
                )

        instance.save()
        return instance


class CreateClassifiedImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassifiedImage
        fields = ('id',)
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance
