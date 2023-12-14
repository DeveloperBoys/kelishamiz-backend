from django.db import models
from django.conf import settings


class Banner(models.Model):
    """
    Model for storing banners with titles, descriptions, images, and URLs.
    """
    title = models.CharField(max_length=150)
    short_description = models.CharField(max_length=350)
    image = models.FileField()
    url = models.URLField()

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image:
            return f"{settings.HOST}{self.image.url}"
        return None
