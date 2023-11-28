from django.contrib import admin

from .models import StartAd, FasterAd, VipAd, AdClassified


admin.site.register(StartAd)
admin.site.register(FasterAd)
admin.site.register(VipAd)
admin.site.register(AdClassified)
