from django.contrib import admin

from .models import CustomOrder
from payme.models import MerchatTransactionsModel

admin.site.register(CustomOrder)
