from django.contrib import admin

from .models import CustomOrder, UserBalance
from payme.models import MerchatTransactionsModel

admin.site.register(CustomOrder)
admin.site.register(UserBalance)
