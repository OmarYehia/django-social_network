from django.db import models
from django.contrib.auth.models import User
from itertools import chain
import random

# Create your models here.
GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='avatar.png')
    background = models.ImageField(
        upload_to='background', default='background.png')
    friends = models.ManyToManyField(
        User, related_name='friends', blank=True)
    bio = models.TextField(default="no bio..")
    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, editable=False, null=True)
    date_of_birth = models.DateField(null=True, editable=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    @property
    def get_username(self):
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

    def get_friends(self):
        return self.friends.all()

    def get_friends_users(self):
        friends_list = [profile for profile in self.get_friends()]
        return friends_list

    def get_my_and_friends_posts(self):
        users = [user for user in self.get_friends()]
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

    def get_proposals_for_friends(self):
        profiles = Profile.objects.all().exclude(user=self.user)
        friends_list = [profile for profile in self.get_friends()]
        available = [
            profile.user for profile in profiles if profile.user not in friends_list]
        random.shuffle(available)
        return available[:3]

    @property
    def friends_count(self):
        return self.get_friends().count()


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class Relationship(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
