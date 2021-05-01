from django.shortcuts import render, redirect
from .models import Post, Like
from profiles.models import Profile
from .forms import PostForm
# Create your views here.


def posts_index(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    posts = Post.objects.filter(author=profile)  # Gets own posts
    # Need to get friends posts
    # get groups posts

    post_form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        print(request.POST)
        if post_form.is_valid():
            post_instance = post_form.save(commit=False)
            post_instance.author = profile
            post_instance.save()

            return redirect("posts:posts-index")

    context = {
        'posts': posts,
        'profile': profile,
        'post_form': post_form
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
