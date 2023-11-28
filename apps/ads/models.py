from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.payments.models import UserBalance
from apps.classifieds.models import Classified


class Ad(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=250)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    top_duration = models.IntegerField(help_text="Number of days in TOP ads")
    bump_ups = models.IntegerField(
        help_text="Number of ad bump ups", blank=True, null=True)
    vip_duration = models.IntegerField(
        help_text="Number of days in VIP ads", blank=True, null=True)

    class Meta:
        verbose_name = "Ad"
        verbose_name_plural = "Ads"

    def __str__(self):
        return self.name


class AdClassified(models.Model):
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)

    start_date = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
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

    def set_end_date(self):
        if not self.end_date:
            self.end_date = self.start_date + \
                timezone.datetime(day=self.ad.top_duration)

    def deduct_ad_cost(self):
        user_balance = UserBalance.objects.filter(
            user=self.classified.owner).last()
        user_balance.balance -= self.ad.cost
        user_balance.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.validate()
            self.set_end_date()
            self.deduct_ad_cost()
        super().save(*args, **kwargs)
