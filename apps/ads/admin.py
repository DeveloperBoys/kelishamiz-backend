from django.contrib import admin

from .models import ClassifiedAd, AdType, TopClassified, AdTypeAttribute


admin.site.register(AdType)
admin.site.register(ClassifiedAd)
admin.site.register(TopClassified)
admin.site.register(AdTypeAttribute)
