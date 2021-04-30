from django.db import models
from profiles.models import Profile


class Post(models.Model):
    title = models.TextField(max_length=250)
    body = models.TextField(max_length=250)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='posts')
    created = created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.title)

