from django.db import models
from django.db import models


class Post(models.Model):
    title = models.TextField(max_length=250)
    body = models.TextField(max_length=250)
    # author

