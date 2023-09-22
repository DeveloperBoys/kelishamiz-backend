from django.db import models


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    views_multiplier = models.IntegerField()
    duration = models.IntegerField(help_text="Duration in days")
    bump_ups = models.IntegerField(help_text="Number of ad bump ups")
    vip_days = models.IntegerField(help_text="Number of days in VIP ads")

    def __str__(self):
        return self.name


class PromotionClassified(models.Model):
    classified = models.ForeignKey()
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
