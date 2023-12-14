from django.db import models
from django.conf import settings

from .base import Base


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
