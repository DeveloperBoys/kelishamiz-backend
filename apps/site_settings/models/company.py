from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _


class Company(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=355)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)

    logo = models.ImageField(upload_to='company/company-logos/', blank=True)

    def __str__(self):
        return self.name

    @property
    def logo_url(self):
        if self.logo:
            return f"{settings.HOST}{self.logo.url}"
        return None


class SocialMediaProfile(models.Model):
    company = models.ForeignKey(
        Company, related_name='social_media_profiles', on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=[
        ('X', 'X'),
        ('YouTube', 'YouTube'),
        ('Facebook', 'Facebook'),
        ('Telegram', 'Telegram'),
        ('Instagram', 'Instagram')
    ])
    icon = models.FileField(upload_to='company/social-media/')
    url = models.URLField()

    class Meta:
        unique_together = ['company', 'platform']

    @property
    def icon_url(self):
        if self.icon:
            return f"{settings.HOST}{self.icon.url}"
        return None


class AppStoreLink(models.Model):
    company = models.ForeignKey(
        Company, related_name='app_links', on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=[
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ])
    logo = models.FileField(upload_to='company/app-store/')
    url = models.URLField()

    class Meta:
        unique_together = ['company', 'platform']

    @property
    def logo_url(self):
        if self.logo:
            return f"{settings.HOST}{self.logo.url}"
        return None
