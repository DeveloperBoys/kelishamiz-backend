from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


from .models import ClassifiedAd
from apps.classifieds.models import Classified


@receiver(pre_save, sender=ClassifiedAd)
def calculate_ended_date_and_is_active(sender, instance, **kwargs):
    now = timezone.now()
    if instance.ended_date is not None:
        instance.is_active = instance.started_date <= now <= instance.ended_date
    else:
        instance.is_active = False


@receiver(post_save, sender=Classified)
def update_top_classifieds(sender, instance, **kwargs):
    """
    Update related TopClassified objects when a Classified is saved.
    """
    top_classified = instance.topclassified

    if top_classified:
        top_classified.check_classified_activity()
