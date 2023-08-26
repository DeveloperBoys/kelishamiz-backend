from rest_framework import serializers

from .models import Category, DynamicField, Ad, AdDetail, AdImage


class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicField
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    currencyType = serializers.CharField(source='currency_type')
    dynamicFields = DynamicFieldSerializer(many=True)

    class Meta:
        model = AdDetail
        fields = ('currencyType', 'price', 'description', 'dynamicFields')


class AdImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField()

    class Meta:
        model = AdImage
        fields = ('imageUrl',)

    def get_imageUrl(self, obj):
        return obj.image.url if obj.image else None


class AdListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    imageUrl = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Ad
        fields = ('title', 'imageUrl', 'price', 'createdAt')

    def get_price(self, obj):
        ad_detail = AdDetail.objects.filter(ad=obj).first()
        return ad_detail.price if ad_detail else None

    def get_imageUrl(self, obj):
        ad_image = AdImage.objects.filter(ad=obj).first()
        return ad_image.image.url if ad_image else None


class AdSerializer(serializers.ModelSerializer):
    detail = AdDetailSerializer(source='addetail', read_only=True)
    images = AdImageSerializer(source='adimage_set', many=True, read_only=True)
    category = serializers.CharField(source='category.name')
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Ad
        fields = ('title', 'category', 'detail', 'images', 'createdAt')


class AdCreateSerializer(serializers.ModelSerializer):
    detail = AdDetailSerializer()
    images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Ad
        fields = ('category', 'title', 'is_active', 'detail', 'images')

    def create(self, validated_data):
        detail_data = validated_data.pop('detail')
        images_data = validated_data.pop('images')

        ad_detail = AdDetail.objects.create(**detail_data)
        ad = Ad.objects.create(addetail=ad_detail, **validated_data)

        for image_data in images_data:
            AdImage.objects.create(ad=ad, image=image_data)

        return ad
