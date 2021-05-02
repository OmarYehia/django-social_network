from django.db import models
from django.contrib.auth.models import User
from itertools import chain
import random


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

    def get_following(self):
        return self.following.all()

    def get_following_users(self):
        following_list = [profile for profile in self.get_following()]
        return following_list

    def get_my_and_following_posts(self):
        users = [user for user in self.get_following()]
        posts = []
        qs = None
        for u in users:
            profile = Profile.objects.get(user=u)
            profile_posts = profile.posts.all()
            posts.append(profile_posts)
        my_posts = self.posts.all()
        posts.append(my_posts)
        if len(posts) > 0:
            qs = sorted(chain(*posts), reverse=True,
                        key=lambda obj: obj.created)
        return qs

    def get_proposals_for_following(self):
        profiles = Profile.objects.all().exclude(user=self.user)
        followers_list = [profile for profile in self.get_following()]
        available = [
            profile.user for profile in profiles if profile.user not in followers_list]
        random.shuffle(available)
        return available[:3]

    @property
    def following_count(self):
        return self.get_following().count()

    def get_followers(self):
        qs = Profile.objects.all()
        followers_list = []
        for profile in qs:
            if self.user in profile.get_following():
                followers_list.append(profile)
        return followers_list

    @property
    def followers_count(self):
        return len(self.get_followers())


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"