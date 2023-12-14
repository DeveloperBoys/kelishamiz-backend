from django.contrib import admin

from .models import (
    Banner,
    Company,
    Locations,
    AppStoreLink,
    SocialMediaProfile,
)

admin.site.register(Banner)
admin.site.register(Company)
admin.site.register(Locations)
admin.site.register(AppStoreLink)
admin.site.register(SocialMediaProfile)
