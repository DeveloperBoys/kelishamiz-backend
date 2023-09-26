from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


from .models import ClassifiedAd, TopClassified
from apps.classifieds.models import Classified


@receiver(pre_save, sender=ClassifiedAd)
def calculate_ended_date_and_is_active(sender, instance, **kwargs):
    now = timezone.now()
    if instance.ended_date is not None:
        instance.is_active = instance.started_date <= now <= instance.ended_date
    else:
        instance.is_active = False


@receiver(post_save, sender=ClassifiedAd)
def update_top_classifieds(sender, instance, created, **kwargs):
    """
    Update related TopClassified objects when a ClassifiedAd is saved and is_active=True.
    """
    if not created:
        try:
            top_classified = instance.classified.topclassified
        except TopClassified.DoesNotExist:
            top_classified = TopClassified(classified=instance.classified)
            top_classified.save()

        if instance.is_active:
            top_classified.is_active = True
        else:
            top_classified.is_active = False

        top_classified.save()
