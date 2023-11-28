from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from apps.payments.models import UserBalance
from apps.classifieds.models import Classified


class Ad(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=250)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    bump_ups = models.IntegerField(
        help_text="Number of ad bump ups", blank=True, null=True)
    top_duration = models.IntegerField(
        help_text="Number of days in TOP ads", blank=True, null=True)

    class Meta:
        abstract = True


class StartAd(Ad):

    class Meta:
        verbose_name = "Start Ad"
        verbose_name_plural = "Start Ads"

    def __str__(self):
        return self.name


class FasterAd(Ad):
    bump_ups = models.IntegerField(
        help_text="Number of ad bump ups")
    top_duration = models.IntegerField(
        help_text="Number of days in TOP ads")

    class Meta:
        verbose_name = "Faster Ad"
        verbose_name_plural = "Faster Ads"

    def __str__(self):
        return self.name


class VipAd(Ad):
    bump_ups = models.IntegerField(
        help_text="Number of ad bump ups")
    top_duration = models.IntegerField(
        help_text="Number of days in TOP ads")
    vip_duration = models.IntegerField(help_text="Number of days in VIP ads")

    class Meta:
        verbose_name = "Vip Ad"
        verbose_name_plural = "Vip Ads"

    def __str__(self):
        return self.name


class AdClassified(models.Model):
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE)
    # ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    ad_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    ad_object_id = models.PositiveIntegerField()
    ad = GenericForeignKey('ad_content_type', 'ad_object_id')

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    @property
    def is_active(self):
        now = timezone.now()
        if self.pk:
            return self.start_date <= now <= self.end_date
        return False

    def validate(self):
        user_balance = UserBalance.objects.filter(
            user=self.classified.owner).last()
        if not user_balance or user_balance.balance < self.ad.cost:
            raise ValidationError("Insufficient balance")

        active_ads = AdClassified.objects.filter(
            classified=self.classified,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        if active_ads.exists():
            raise ValidationError(
                "Classified already has an active purchased ad")

    def deduct_ad_cost(self):
        user_balance = UserBalance.objects.filter(
            user=self.classified.owner).last()
        user_balance.balance -= self.ad.cost
        user_balance.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.validate()
            self.deduct_ad_cost()
        super().save(*args, **kwargs)
