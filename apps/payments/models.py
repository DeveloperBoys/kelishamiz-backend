from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
