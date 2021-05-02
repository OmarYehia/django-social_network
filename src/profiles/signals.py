from .models import Profile, Relationship
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile_instance = Profile.objects.create(first_name=instance.first_name, last_name=instance.last_name,
                                                  email=instance.email, user=instance)
        instance.profile = profile_instance
        instance.save()


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, *args, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()
