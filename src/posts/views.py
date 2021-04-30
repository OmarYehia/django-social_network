from django.shortcuts import render
from posts.models import Post


def posts_view(request):
    posts = Post.objects.all()
    return render(request, 'posts/main.html', {'posts':posts})

