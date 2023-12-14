from django.db import models


class Locations(models.Model):
    name = models.CharField(max_length=150)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
