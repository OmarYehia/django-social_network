from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
# Create your models here.


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[
                              FileExtensionValidator(['jpg', 'jpeg', 'png'])], blank=True, null=True)
    likes = models.ManyToManyField(
        Profile, related_name='likes', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.pk)

    @property
    def get_total_likes(self):
        return self.likes.all().count()

    @property
    def get_total_comments(self):
        return self.comments.all().count()

    class Meta:
        ordering = ('-created_at',)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=500)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class Like(models.Model):
    LIKE_CHOICES = (
        ('Like', 'Like'),
        ('Unlike', 'Unlike')
    )

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.value}-Post id: {self.post}"
