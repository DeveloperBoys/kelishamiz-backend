from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Base):
    name = models.CharField(max_length=250)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.FileField(null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Ad(Base):
    """
    In this Ad model, the main fields of the ad placed by the user are stored.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Ad"
        verbose_name_plural = "Ads"


class CategorySpecificModel(Base):
    """
    All models that inherit from this model are created for additional fields of the ad that the user must place.
    """

    ad = models.OneToOneField(
        Ad, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        abstract = True


class TransportCategory(CategorySpecificModel):
    """
    Transportation Model
    """

    class Meta:
        verbose_name = "Transportation Category"
        verbose_name_plural = "Transportation Categories"


class RECategory(CategorySpecificModel):
    """
    Real Estate Model
    """

    class Meta:
        verbose_name = "Real Estate Category"
        verbose_name_plural = "Real Estate Categories"


class WASCategory(CategorySpecificModel):
    """
    Work and Services Model
    """

    class Meta:
        verbose_name = "Work and Services Category"
        verbose_name_plural = "Work and Services Categories"


class EATCategory(CategorySpecificModel):
    """
    Electronics and Technology Model
    """

    class Meta:
        verbose_name = "Electronics and Technology Category"
        verbose_name_plural = "Electronics and Technology Categories"


class HGAFCategory(CategorySpecificModel):
    """
    Home, Garden and Furniture Model
    """

    class Meta:
        verbose_name = "Home, Garden and Furniture Category"
        verbose_name_plural = "Home, Garden and Furniture Categories"


class CGCategory(CategorySpecificModel):
    """
    Construction Goods Model
    """

    class Meta:
        verbose_name = "Construction Goods Category"
        verbose_name_plural = "Construction Goods Categories"


class ProductionCategory(CategorySpecificModel):
    """
    Production Model
    """

    class Meta:
        verbose_name = "Production Category"
        verbose_name_plural = "Production Categories"


class PICategory(CategorySpecificModel):
    """
    Personal Items Model
    """

    class Meta:
        verbose_name = "Personal Items Category"
        verbose_name_plural = "Personal Items Categories"


class OCategory(CategorySpecificModel):
    """
    Others Model
    """

    class Meta:
        verbose_name = "Others Category"
        verbose_name_plural = "Others Categories"
