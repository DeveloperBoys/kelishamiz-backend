# from django.dispatch import receiver
# from django.db.models.signals import post_save

# from payme.models import MerchantTransactionsModel

# from .models import CustomOrder, UserBalance


# @receiver(post_save, sender=MerchantTransactionsModel)
# def update_user_balance(sender, instance, created, **kwargs):
#     if instance.state == 2:
#         order = CustomOrder.objects.get(id=instance.order_id)
#         user = order.user

#         user_balance = UserBalance.objects.get_or_create(user=user)

#         user_balance.balance += instance.amount
#         user_balance.save()
