from django.db import models
from django.utils import timezone


from apps.classifieds.models import Classified


class AdTypeAttribute(models.Model):
    """
    Model for storing attributes of advertisement types.
    """
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Ad Type Attribute"
        verbose_name_plural = "Ad Type Attributes"

    def __str__(self):
        return self.name


class AdType(models.Model):
    """
    Model for defining advertisement types with names, validity periods, and attributes.
    """

    name = models.CharField(max_length=250)
    icon = models.FileField(upload_to="ads/adtype/")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    short_description = models.CharField(max_length=250)
    validity_period = models.IntegerField(
        blank=True,
        null=True,
        help_text="Validity period for the advertisement in days"
    )
    attributes = models.ManyToManyField(AdTypeAttribute, blank=True)

    class Meta:
        verbose_name = "Ad Type"
        verbose_name_plural = "Ad Types"

    def __str__(self):
        return self.name


class TopClassified(models.Model):
    classified = models.OneToOneField(
        Classified, on_delete=models.CASCADE, related_name='topclassified')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Top Classified"
        verbose_name_plural = "Top Classifieds"

    def __str__(self):
        return self.classified.title

    def check_classified_activity(self):
        self.is_active = self.classified.is_active
        self.save()


class ClassifiedAd(models.Model):
    classified = models.OneToOneField(
        Classified, related_name='ad', on_delete=models.CASCADE)
    ad_type = models.OneToOneField(
        AdType, related_name='ad', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    started_date = models.DateTimeField(blank=True, null=True)
    ended_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Classified Ad"
        verbose_name_plural = "Classified Ads"

    def save(self, *args, **kwargs):
        if not self.started_date:
            self.started_date = timezone.now()

        self.calculate_ended_date()
        super(ClassifiedAd, self).save(*args, **kwargs)

    def calculate_ended_date(self):
        validity_period = self.ad_type.validity_period
        if validity_period is not None:
            self.ended_date = self.started_date + \
                timezone.timedelta(days=validity_period)
        else:
            self.ended_date = None
