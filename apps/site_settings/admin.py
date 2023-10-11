from django.contrib import admin

from .models import SocialMedia, AppStoreLink, CompanyInfo, Banner

admin.site.register(SocialMedia)
admin.site.register(AppStoreLink)
admin.site.register(CompanyInfo)
admin.site.register(Banner)
