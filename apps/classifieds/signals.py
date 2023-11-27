from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Classified, PENDING
from tasks import trigger_bot_notification


@receiver(pre_save, sender=Classified)
def trigger_bot_post(sender, instance, **kwargs):
    if instance.status == PENDING:
        trigger_bot_notification.delay(instance.id)
