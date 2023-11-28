from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Score

@receiver(post_save, sender=User)
def create_user_score(sender, instance, created, **kwargs):
    if created:
        Score.objects.create(user=instance, score=0)