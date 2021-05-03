from django.db import models
from profiles.models import Profile

# Create your models here.


class Thread(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='+')


class Message(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    sender_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='+')
    receiver_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
