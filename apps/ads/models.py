from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.classifieds.models import Classified


class Ad(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    views_multiplier = models.IntegerField()
    bump_ups = models.IntegerField(help_text="Number of ad bump ups")
    duration = models.IntegerField(help_text="Number of days in VIP ads")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# class VipAd(Ad):
#     duration = models.IntegerField(help_text="Number of days in VIP ads")

#     class Meta:
#         verbose_name = "Vip Ad"
#         verbose_name_plural = "Vip Ads"

#     def __str__(self):
#         return self.name


class AdClassified(models.Model):
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    @property
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def validate_ad(self):
        try:
            if not self.ad.is_active:
                raise ValidationError("Ad is no longer active")
        except Ad.DoesNotExist:
            raise ValidationError("Invalid ad")

        # Check user balance
        if self.classified.user.balance < self.ad.cost:
            raise ValidationError("Insufficient balance for ad cost")

        # Check classified not already promoted
        other_ads = AdClassified.objects.filter(
            classified=self.classified,
            is_active=True
        )
        if other_ads.exists():
            raise ValidationError("Classified already has an active ad")

    def clean(self):
        self.validate_ad()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
