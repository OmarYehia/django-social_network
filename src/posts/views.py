from django.shortcuts import render, redirect
from .models import Post, Like
from profiles.models import Profile
# Create your views here.


def posts_index(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    posts = Post.objects.filter(author=profile)  # Gets own posts
    # Need to get friends posts
    # get groups posts

    context = {
        'posts': posts,
        'profile': profile
    }

    return render(request, 'posts/index.html', context)


def like_unlike_post(request):
    user = request.user

    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post.likes.all():
            post.likes.remove(profile)
        else:
            post.likes.add(profile)

        like, created = Like.objects.get_or_create(
            user=profile, post_id=post_id)

        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        else:
            like.value = "Like"

        post.save()
        like.save()

    return redirect('posts:posts-index')
