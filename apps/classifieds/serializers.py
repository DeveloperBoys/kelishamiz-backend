from rest_framework import serializers

from .models import (
    Category,
    Classified,
    DynamicField,
    ClassifiedImage,
    ClassifiedDetail,
    PENDING,
    DRAFT,
    DELETED
)


class ChildCategorySerializer(serializers.ModelSerializer):
    iconUrl = serializers.CharField(source="icon_url", read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'iconUrl')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    iconUrl = serializers.CharField(source="icon_url", read_only=True)
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

        if request and request.method == 'GET':
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
        fields = ('id', 'classified', 'image', 'imageUrl',)
        read_only_fields = ('id',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        # Check if the request method is GET
        if request and request.method == 'GET':
            # Remove 'image' field for GET requests
            data.pop('image', None)

        return data

    def validate(self, data):
        if not self.instance:
            classified = data['classified']
            if classified.status != DRAFT:
                raise serializers.ValidationError(
                    'Classified image must be in draft status')

        return data

    def create(self, validated_data):
        # Create a new image instance
        return ClassifiedImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update an existing image instance
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class ClassifiedDetailSerializer(serializers.ModelSerializer):
    currencyType = serializers.CharField(source='currency_type')
    dynamicFields = serializers.SerializerMethodField(source='dynamic_fields')
    images = serializers.SerializerMethodField()

    class Meta:
        model = ClassifiedDetail
        fields = ('currencyType', 'price', 'description',
                  'dynamicFields', 'images')

    def get_dynamicFields(self, obj):
        dynamic_fields = DynamicField.objects.filter(classified_detail=obj)
        if dynamic_fields.exists():
            return DynamicFieldSerializer(dynamic_fields, many=True).data
        return None

    def get_images(self, obj):
        images = ClassifiedImage.objects.filter(classified=obj.classified)
        if images.exists():
            request = self.context.get('request')
            return ClassifiedImageSerializer(images, many=True, context={'request': request}).data
        return None


class ClassifiedListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(read_only=True)
    imageUrl = serializers.SerializerMethodField(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    isLiked = serializers.BooleanField(source='is_liked')

    class Meta:
        model = Classified
        fields = ('id', 'category', 'owner', 'title', 'imageUrl',
                  'price', 'isLiked', 'createdAt')
        read_only_fields = ('id',)

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

        detail_data = validated_data.get('classifieddetail', {})
        detail_serializer = ClassifiedDetailSerializer(
            instance=instance.classifieddetail, data=detail_data, partial=True
        )
        if detail_serializer.is_valid():
            detail_serializer.save()

        return instance


class DeleteClassifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classified
        # Only include the 'id' field to identify the classified
        fields = ('id',)

    def update(self, instance, validated_data):
        # Change the status of the classified to 'DELETE'
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
    dynamicFields = DynamicFieldSerializer(
        many=True, source="dynamicfield_set")

    class Meta:
        model = ClassifiedDetail
        fields = ('id', 'classified', 'currency_type', 'price',
                  'is_negotiable', 'description', 'dynamicFields')
        read_only_fields = ('id',)

    def validate(self, data):
        if not self.instance:
            classified = data['classified']
            if classified.status != DRAFT:
                raise serializers.ValidationError(
                    "Classified detail must be in draft status")

        return data

    def create(self, validated_data):
        dynamic_fields = validated_data.pop('dynamicfield_set')
        classified = validated_data.pop('classified')
        currency_type = validated_data.pop('currency_type')
        price = validated_data.pop('price')
        is_negotiable = validated_data.pop('is_negotiable')
        description = validated_data.pop('description')
        classified_detail = ClassifiedDetail.objects.create(
            classified=classified,
            currency_type=currency_type,
            price=price,
            is_negotiable=is_negotiable,
            description=description
        )

        for dynamic_field_data in dynamic_fields:
            DynamicField.objects.create(
                key=dynamic_field_data['key'],
                value=dynamic_field_data['value'],
                classified_detail=classified_detail
            )

        # Attach dynamic fields to the detail
        classified_detail.classified.status = PENDING
        classified_detail.classified.save()
        return classified_detail

    def update(self, instance, validated_data):
        instance.currency_type = validated_data.get(
            'currency_type', instance.currency_type)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get(
            'description', instance.description)

        # Update dynamic fields
        new_dynamic_fields = validated_data.get('dynamicfield_set')
        if new_dynamic_fields:
            for dynamic_field_data in new_dynamic_fields:
                dynamic_field, created = DynamicField.objects.get_or_create(
                    classified_detail=instance,
                    key=dynamic_field_data['key'],  # Assuming 'key' is unique
                    defaults={'value': dynamic_field_data['value']}
                )
                if not created:
                    dynamic_field.value = dynamic_field_data['value']
                    dynamic_field.save()

        instance.classified.status = PENDING
        instance.classified.save()

        instance.save()
        return instance
