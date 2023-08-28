from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import ClassifiedLike


@receiver(post_save, sender=ClassifiedLike)
def update_classified_on_like(sender, instance, created, **kwargs):
    if instance.is_active:
        instance.classified.is_liked = True
    elif not ClassifiedLike.objects.filter(classified=instance.classified, is_active=True).exists():
        instance.classified.is_liked = False
    instance.classified.save()


post_save.connect(update_classified_on_like, sender=ClassifiedLike)
