from django.contrib import admin

from .models import CustomOrder, UserBalance

admin.site.register(CustomOrder)
admin.site.register(UserBalance)
