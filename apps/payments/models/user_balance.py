from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "User Balance"
        verbose_name_plural = "Users Balance"
