from django.contrib import admin

from .models import ClassifiedAd, AdType


admin.site.register(AdType)
admin.site.register(ClassifiedAd)
