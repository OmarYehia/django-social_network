from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='avatar.png')
    background = models.ImageField(
        upload_to='background', default='background.png')
    following = models.ManyToManyField(
        User, related_name='following', blank=True)
    bio = models.TextField(default="no bio..")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    @property
    def get_total_posts(self):
        return self.posts.all().count()

    @property
    def get_all_author_posts(self):
        return self.posts.all()

    @property
    def get_total_likes_given_number(self):
        likes = self.like_set.all()
        total = 0
        for i in likes:
            if i.value == "Like":
                total += 1
        return total

    @property
    def get_total_likes_recieved_number(self):
        posts = self.posts.all()
        total = 0
        for i in posts:
            total += i.get_total_likes
        return total
