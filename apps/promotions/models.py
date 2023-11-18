from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.classifieds.models import Classified


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    views_multiplier = models.IntegerField()
    duration = models.IntegerField(help_text="Duration in days")
    bump_ups = models.IntegerField(help_text="Number of ad bump ups")
    vip_duration = models.IntegerField(help_text="Number of days in VIP ads")

    def __str__(self):
        return self.name


class PromotionClassified(models.Model):
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    @property
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def validate_promotion(self):
        try:
            if not self.promotion.is_active:
                raise ValidationError("Promotion is no longer active")
        except Promotion.DoesNotExist:
            raise ValidationError("Invalid promotion")

        # Check user balance
        if self.classified.user.balance < self.promotion.cost:
            raise ValidationError("Insufficient balance for promotion cost")

        # Check classified not already promoted
        other_promos = PromotionClassified.objects.filter(
            classified=self.classified,
            is_active=True
        )
        if other_promos.exists():
            raise ValidationError("Classified already has an active promotion")

    def clean(self):
        self.validate_promotion()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
