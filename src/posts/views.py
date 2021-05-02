from django.shortcuts import render, redirect
from .models import Post, Like, Comment
from profiles.models import Profile
from .forms import PostForm, CommentForm
from django.db.models import Q
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


def posts_index(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    friend_profiles = []
    friends = profile.following.all()
    for friend in friends:
        friend_profile = Profile.objects.get(user=friend)
        friend_profiles.append(friend_profile)

    posts = Post.objects.filter(
        Q(author=profile) |
        Q(author__in=friend_profiles))
    # get groups posts

    post_form = PostForm()
    comment_form = CommentForm()
    post_added = False

    if 'submit_post_form' in request.POST:
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_instance = post_form.save(commit=False)
            post_instance.author = profile
            post_instance.save()
            post_added = True
            return redirect('posts:posts-index')

    elif 'submit_comment_form' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            post_id = request.POST.get("post_id")
            comment_instance = comment_form.save(commit=False)
            comment_instance.user = profile
            comment_instance.post = Post.objects.get(id=post_id)
            comment_instance.save()
            return redirect('posts:posts-index')

    context = {
        'posts': posts,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'post_added': post_added
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


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('posts:posts-index')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        if not post.author.user == self.request.user:
            messages.warning(
                self.request, 'You can delete only your own posts.')

        return post


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:posts-index')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You can update only your own posts.')
            return super().form_invalid(form)


def CommentDelete(request, pk):
    comment = Comment.objects.get(pk=pk)
    logged_user_profile = Profile.objects.get(user=request.user)
    if comment.user == logged_user_profile:
        comment.delete()

    return redirect('posts:posts-index')
