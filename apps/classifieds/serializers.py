from rest_framework import serializers

from .tasks import upload_classified_images
from .models import (
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
        fields = ('id', 'name', 'slug', 'iconUrl')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    iconUrl = serializers.URLField(source="icon_url", read_only=True)
    childs = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'slug', 'icon', 'iconUrl', 'childs')
        read_only_fields = ('id', 'slug')

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
        fields = ('key', 'value')


class ClassifiedImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.URLField(source="image_url", read_only=True)

    class Meta:
        model = ClassifiedImage
        fields = ('id', 'image', 'imageUrl',)
        read_only_fields = ('id',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method != 'GET':
            data.pop('imageUrl', None)
        else:
            data.pop('image', None)

        return data

    def validate(self, data):
        if not self.instance:
            classified = data['classified']
            if classified.status != DELETED:
                raise serializers.ValidationError(
                    'Classified image must be in deleted status')

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
    currencyType = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    isLiked = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Classified
        fields = ('id', 'category', 'owner', 'title', 'slug', 'images', 'price',
                  'currencyType', 'isLiked', 'views', 'location', 'createdAt')
        read_only_fields = ('id', 'slug', 'views')

    def get_isLiked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.classifiedlike_set.filter(
                user_id=user.id, is_active=True).exists()
        return False

    def get_price(self, obj):
        classified_detail = ClassifiedDetail.objects.filter(
            classified=obj).first()
        return classified_detail.price if classified_detail else None

    def get_currencyType(self, obj):
        classified_detail = ClassifiedDetail.objects.filter(
            classified=obj).first()
        return classified_detail.currency_type if classified_detail else None

    def get_category(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            return obj.category.name
        return obj.category.pk

    def get_images(self, obj):
        images = obj.images.order_by('-id')[:5]
        if images:
            request = self.context.get('request')
            return ClassifiedImageSerializer(images, many=True, context={'request': request}).data
        return None

    def get_location(self, obj):
        classified_detail = ClassifiedDetail.objects.select_related(
            'location').filter(classified=obj).first()
        if classified_detail:
            return classified_detail.location.name
        return None


class ClassifiedSerializer(serializers.ModelSerializer):
    detail = ClassifiedDetailSerializer()
    isLiked = serializers.SerializerMethodField(read_only=True)
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

    def get_isLiked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.classifiedlike_set.filter(
                user_id=user.id, is_active=True).exists()
        return False

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


class ClassifiedCreateSerializer(serializers.Serializer):
    category = serializers.IntegerField()
    title = serializers.CharField(max_length=150)
    dynamicFields = DynamicFieldSerializer(many=True, required=False)
    currencyType = serializers.CharField()
    isNegotiable = serializers.BooleanField(required=False)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    description = serializers.CharField()
    location = serializers.IntegerField()

    def create(self, validated_data):
        dynamic_fields = validated_data.pop('dynamicFields', [])
        currency_type = validated_data.pop('currencyType')
        is_negotiable = validated_data.pop('isNegotiable', False)
        price = validated_data.pop('price')
        description = validated_data.pop('description')
        location_id = validated_data.pop('location')
        title = validated_data.pop('title')
        category = validated_data.pop('category')
        user = validated_data.pop('owner')
        images = validated_data.pop('images', [])

        classified = Classified.objects.create(
            category_id=category,
            title=title,
            owner=user
        )

        classified_detail = ClassifiedDetail.objects.create(
            classified=classified,
            currency_type=currency_type,
            is_negotiable=is_negotiable,
            price=price,
            description=description,
            location_id=location_id
        )

        for dynamic_field in dynamic_fields:
            DynamicField.objects.create(
                classified_detail=classified_detail, **dynamic_field)

        image_data_list = [
            {'name': f.name, 'content': f.read()} for f in images
        ]
        upload_classified_images.delay(classified.id, image_data_list)

        classified.status = PENDING
        classified.save()

        return classified
