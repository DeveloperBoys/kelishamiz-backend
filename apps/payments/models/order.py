from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"ORDER ID: {self.id}, USER ID: {self.user.id}, AMOUNT: {self.amount}"
