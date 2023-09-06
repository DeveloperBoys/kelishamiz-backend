from django.db import models


class SocialMedia(models.Model):
    """
    Model for storing social media profiles.
    """
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Medias"

    def __str__(self) -> str:
        return self.name


class AppStoreLink(models.Model):
    """
    Model for storing links to mobile apps on the App Store and Google Play Store.
    """
    app_name = models.CharField(max_length=255)
    ios_url = models.URLField(blank=True, null=True)
    android_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "App Store Link"
        verbose_name_plural = "App Store Links"

    def __str__(self) -> str:
        return self.app_name


class CompanyInfo(models.Model):
    """
    Model for storing company information, including contact details and app links.
    """
    phone_number = models.CharField(max_length=20)

    social_media = models.ManyToManyField(SocialMedia, blank=True)
    app_links = models.ManyToManyField(AppStoreLink, blank=True)

    logo = models.FileField(upload_to="company/logo")

    class Meta:
        verbose_name = "Company Info"
        verbose_name_plural = "Company Info"

    def __str__(self) -> str:
        return "Company Info"


class Banner(models.Model):
    title = models.CharField(max_length=150)
    image = models.FileField()


class AdType(models.Model):
    ...
