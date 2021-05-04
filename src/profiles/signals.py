from .models import Profile, Relationship
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile_instance = Profile.objects.create(first_name=instance.first_name, last_name=instance.last_name,
                                                  email=instance.email, slug=instance.username, user=instance)
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


@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()
