from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Base):
    """
    Category model to represent main categories and subcategories.
    """
    name = models.CharField(max_length=250)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.FileField(
        upload_to='ads/category/icons/', null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class DynamicField(models.Model):
    """
    DynamicField model for storing custom key-value attributes.
    """
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)


class Ad(Base):
    """
    Ad model to store basic advertisement information.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Ad"
        verbose_name_plural = "Ads"


class AdDetail(Base):
    """
    AdDetail model to store detailed information about advertisements.
    """
    ad = models.OneToOneField(
        Ad, related_name='addetail', on_delete=models.CASCADE)
    currency_type = models.CharField(
        max_length=3, choices=(("usd", "USD"), ("uzs", "UZS")))
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    dynamicFields = models.ManyToManyField(DynamicField, blank=True)

    class Meta:
        verbose_name = "Ad Detail"
        verbose_name_plural = "Ad Details"


class AdImage(Base):
    """
    AdImage model to associate images with advertisements.
    """
    ad = models.ForeignKey(Ad, related_name='adimage_set',
                           on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ads/ad/images/')

    class Meta:
        verbose_name = "Ad Image"
        verbose_name_plural = "Ad Images"
