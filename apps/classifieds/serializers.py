from rest_framework import serializers

from .models import Category, DynamicField, Classified, ClassifiedDetail, ClassifiedImage


class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicField
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ClassifiedDetailSerializer(serializers.ModelSerializer):
    currencyType = serializers.CharField(source='currency_type')
    dynamicFields = DynamicFieldSerializer(many=True)

    class Meta:
        model = ClassifiedDetail
        fields = ('currencyType', 'price', 'description', 'dynamicFields')


class ClassifiedImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField()

    class Meta:
        model = ClassifiedImage
        fields = ('imageUrl',)

    def get_imageUrl(self, obj):
        return obj.image.url if obj.image else None


class ClassifiedListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    imageUrl = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Classified
        fields = ('title', 'imageUrl', 'price', 'createdAt')

    def get_price(self, obj):
        classified_detail = ClassifiedDetail.objects.filter(
            classified=obj).first()
        return classified_detail.price if classified_detail else None

    def get_imageUrl(self, obj):
        classified_image = ClassifiedImage.objects.filter(
            classified=obj).first()
        return classified_image.image.url if classified_image else None


class ClassifiedSerializer(serializers.ModelSerializer):
    detail = ClassifiedDetailSerializer(
        source='classifieddetail', read_only=True)
    images = ClassifiedImageSerializer(
        source='classifiedimage_set', many=True, read_only=True)
    category = serializers.CharField(source='category.name')
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Classified
        fields = ('title', 'category', 'detail', 'images', 'createdAt')


class ClassifiedCreateSerializer(serializers.ModelSerializer):
    detail = ClassifiedDetailSerializer()
    images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Classified
        fields = ('category', 'title', 'is_active', 'detail', 'images')

    def create(self, validated_data):
        detail_data = validated_data.pop('detail')
        images_data = validated_data.pop('images')

        classified_detail = ClassifiedDetail.objects.create(**detail_data)
        classified = Classified.objects.create(
            classifieddetail=classified_detail, **validated_data)

        for image_data in images_data:
            ClassifiedImage.objects.create(
                classified=classified, image=image_data)

        return classified
