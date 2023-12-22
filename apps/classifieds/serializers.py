from rest_framework import serializers

from .models import (
    PENDING,
    DELETED,
    Category,
    Classified,
    DynamicField,
    ClassifiedImage,
    ClassifiedDetail,
)
from apps.users.models import User
from .tasks import upload_classified_images
from apps.site_settings.models import Locations
from apps.users.serializers import UserDataSerializer


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
        fields = ('id', 'key', 'value')
        read_only_fields = ('id',)


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
    isNegotiable = serializers.BooleanField(source="is_negotiable")
    images = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = ClassifiedDetail
        fields = ('currencyType', 'price', 'description',
                  'dynamicFields', 'isNegotiable', 'location', 'images')

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
    ownerData = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Classified
        fields = ('id', 'title', 'category', 'detail',
                  'ownerData', 'isLiked', 'createdAt')
        read_only_fields = ('id',)

    def get_ownerData(self, obj):
        owner = User.objects.get(pk=obj.owner.pk)
        return ClassifiedOwnerSerializer(owner).data

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


class DeleteClassifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classified
        fields = ('id',)

    def update(self, instance, validated_data):
        instance.status = DELETED
        instance.save()
        return instance


class ClassifiedCreateSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    title = serializers.CharField(max_length=150)
    dynamicFields = DynamicFieldSerializer(many=True, required=False)
    images = ClassifiedImageSerializer(many=True, required=False)
    currencyType = serializers.ChoiceField(
        choices=(("USD", "usd"), ("UZS", "uzs")))
    isNegotiable = serializers.BooleanField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    description = serializers.CharField()
    location = serializers.PrimaryKeyRelatedField(
        queryset=Locations.objects.all()
    )

    class Meta:
        exclude = ['images']

    def create(self, validated_data):
        dynamic_fields = validated_data.pop('dynamicFields', [])

        request = self.context['request']
        owner = request.user

        classified = Classified.objects.create(
            category=validated_data['category'],
            title=validated_data['title'],
            owner=owner,
        )

        detail = ClassifiedDetail.objects.create(
            classified=classified,
            currency_type=validated_data['currencyType'],
            is_negotiable=validated_data['isNegotiable'],
            price=validated_data['price'],
            description=validated_data['description'],
            location=validated_data['location']
        )

        for dynamic_field in dynamic_fields:
            DynamicField.objects.create(
                classified_detail=detail,
                **dynamic_field
            )

        images = request.FILES.getlist('images')
        upload_classified_images.delay(classified.id, images)

        return classified

    def update(self, instance, validated_data):
        dynamic_fields = validated_data.pop('dynamicFields', [])

        detail = instance.detail

        detail.currency_type = validated_data.get(
            'currencyType', detail.currency_type)
        detail.is_negotiable = validated_data.get(
            'isNegotiable', detail.is_negotiable)
        detail.price = validated_data.get('price', detail.price)
        detail.description = validated_data.get(
            'description', detail.description)
        detail.location = validated_data.get('location', detail.location)

        detail.save()

        for dynamic_field in dynamic_fields:
            field_id = dynamic_field.get("id")
            if field_id:
                DynamicField.objects.filter(
                    id=field_id).update(**dynamic_field)
            else:
                DynamicField.objects.create(
                    classified_detail=detail, **dynamic_field)

        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.save()

        return instance


class ClassifiedOwnerSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name', required=True)
    lastName = serializers.CharField(source='last_name', required=True)
    profileImage = serializers.FileField(
        source='profile_image_url', required=False)
    phoneNumber = serializers.CharField(source='phone_number', required=True)

    class Meta:
        model = User
        fields = ('id', 'firstName', 'lastName',
                  'email', 'phoneNumber', 'profileImage')
        read_only_fields = ('id',)
