from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from user_profile.models import Image



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Image.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.image.save()