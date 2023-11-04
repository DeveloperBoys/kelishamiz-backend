from django.contrib import admin

from .models import (
    Banner,
    Company,
    AppStoreLink,
    SocialMediaProfile,
)

admin.site.register(Banner)
admin.site.register(Company)
admin.site.register(AppStoreLink)
admin.site.register(SocialMediaProfile)
