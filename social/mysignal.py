from django.contrib.auth.models import User
from django.db.models.signals import post_save
from social.models import MyProfile
from django.dispatch.dispatcher import receiver


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwa):
    if created:
        MyProfile.objects.create(user=instance , name = instance.username)
