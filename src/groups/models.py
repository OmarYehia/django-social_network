from django.db import models
from profiles.models import Profile

# Create your models here.


class Group(models.Model):
    users = models.ManyToManyField(Profile, blank=True, related_name='groups')
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='+')
    name = models.CharField(max_length=50)
    overview = models.TextField(
        max_length=500, default='No overview available', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # posts have reverse relation in posts.models --> post_set.all() to get all posts

    def __str__(self):
        return self.name
