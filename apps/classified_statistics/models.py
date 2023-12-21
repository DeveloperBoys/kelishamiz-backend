from django.db import models
from django.contrib.auth import get_user_model

from apps.classifieds.models import Classified


User = get_user_model()


class ClassifiedView(models.Model):
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Classified View"
        verbose_name_plural = "Classified Views"

    def __str__(self):
        return f"Classfied: {self.classified.title} - Viewed AT: {self.viewed_at}"


class ClassifiedLike(models.Model):
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Classified Like"
        verbose_name_plural = "Classified Likes"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'classified'], name='unique_user_classified_like')
        ]

    def __str__(self):
        return f"User UUID: {self.user.guid} - Classified: {self.classified.title}"
