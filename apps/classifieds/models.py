from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


DRAFT, PENDING, APPROVED, REJECTED = (
    "draft", "pending", "approved", "rejected"
)


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
        'self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    icon = models.FileField(
        upload_to='classifieds/category/icons/', null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @property
    def icon_url(self):
        if self.icon:
            return f"{settings.HOST}{self.icon.url}"
        return None


class DynamicField(Base):
    """
    DynamicField model for storing custom key-value attributes.
    """
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Dynamic Field"
        verbose_name_plural = "Dynamic Fields"

    def __str__(self):
        return f"key: {self.key} - value: {self.value}"


class Classified(Base):
    """
    Classified model to store basic classifieds information.
    """
    CLASSIFIED_STATUS = (
        (DRAFT, DRAFT),
        (PENDING, PENDING),
        (APPROVED, APPROVED),
        (REJECTED, REJECTED)
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=CLASSIFIED_STATUS, default=DRAFT)
    title = models.CharField(max_length=150)
    is_liked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Classified"
        verbose_name_plural = "Classifieds"

    def __str__(self) -> str:
        return self.title
    
    def can_edit(self):
        return self.status == DRAFT

    def can_delete(self):
        return self.status == DRAFT


class ClassifiedDetail(Base):
    """
    ClassifiedDetail model to store detailed information about classifieds.
    """
    classified = models.OneToOneField(
        Classified, related_name='classifieddetail', on_delete=models.CASCADE)
    currency_type = models.CharField(
        max_length=3, choices=(("usd", "USD"), ("uzs", "UZS")))
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_negotiable = models.BooleanField(default=False)
    description = models.TextField()
    dynamic_fields = models.ManyToManyField(
        DynamicField, blank=True, related_name='classified_details')

    class Meta:
        verbose_name = "Classified Detail"
        verbose_name_plural = "Classified Details"


class ClassifiedImage(Base):
    """
    ClassifiedImage model to associate images with classifieds.
    """
    classified = models.ForeignKey(Classified, related_name='classifiedimage_set',
                                   on_delete=models.CASCADE)
    image = models.ImageField(upload_to='classifieds/images/')

    class Meta:
        verbose_name = "Classified Image"
        verbose_name_plural = "Classified Images"

    def __str__(self) -> str:
        return self.classified.title

    @property
    def image_url(self):
        if self.image:
            return f"{settings.HOST}{self.image.url}"
        return None
