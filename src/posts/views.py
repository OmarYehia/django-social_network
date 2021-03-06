from django.shortcuts import render, redirect
from .models import Post, Like, Comment, Notifications, CustomProfanity
from profiles.models import Profile
from .forms import PostForm, CommentForm
from django.db.models import Q
from django.views.generic import DeleteView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from better_profanity import profanity
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="/login")
def posts_index(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    friend_profiles = []
    friends = profile.friends.all()
    for friend in friends:
        friend_profile = Profile.objects.get(user=friend)
        friend_profiles.append(friend_profile)

    groups = profile.groups.all()

    posts = Post.objects.filter(
        Q(author=profile) |
        Q(author__in=friend_profiles) |
        Q(group__in=groups)
    )

    post_form = PostForm()
    comment_form = CommentForm()
    post_added = False

    # Custom profanity words
    custom_badwords = CustomProfanity.objects.values_list(
        'bad_word', flat=True)
    profanity.load_censor_words(custom_badwords)

    if 'submit_post_form' in request.POST:
        post_form = PostForm(request.POST, request.FILES)
        valid = post_form.is_valid()

        if profanity.contains_profanity(post_form.cleaned_data.get('content')):
            custom_profanity_error = 'Please remove any profanity/swear words. (Added by an admin. Contact an admin if you believe this is wrong.)'
            valid = False
            post_form.errors['content'] = custom_profanity_error

        if valid:
            post_instance = post_form.save(commit=False)
            post_instance.author = profile
            post_instance.save()
            post_added = True
            return redirect(request.headers.get('Referer'))

    elif 'submit_comment_form' in request.POST:
        comment_form = CommentForm(request.POST)
        valid = comment_form.is_valid()

        if profanity.contains_profanity(comment_form.cleaned_data.get('body')):
            custom_profanity_error = 'Please remove any profanity/swear words. (Added by an admin. Contact an admin if you believe this is wrong.)'
            valid = False
            comment_form.errors['body'] = custom_profanity_error

        if valid:
            post_id = request.POST.get("post_id")
            comment_instance = comment_form.save(commit=False)
            comment_instance.user = profile
            comment_instance.post = Post.objects.get(id=post_id)
            comment_instance.save()
            notification = Notifications.objects.create(
                notification_type=2, from_user=request.user, to_user=comment_instance.post.author.user,
                post=comment_instance.post)
            return redirect(request.headers.get('Referer'))

    context = {
        'posts': posts,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'post_added': post_added,
    }

    return render(request, 'posts/index.html', context)


@login_required(login_url="/login")
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
        notification = Notifications.objects.create(
            notification_type=1, from_user=request.user, to_user=post.author.user, post=post)

    return redirect(request.headers.get('Referer'))


class PostDeleteView(DeleteView):
    def get(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
        except:
            return render(request, 'main/not_found.html')

        if post.group:
            if not post.group.owner.user == self.request.user and not post.author.user == self.request.user:
                messages.warning(
                    request, 'You can only delete your own posts or posts in a group you own.')
        elif not post.author.user == self.request.user:
            messages.warning(
                request, 'You can only delete your own posts.')

        return render(request, 'posts/confirm_delete.html')

    def post(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return redirect(request.POST.get('referer'))
        except:
            return render(request, 'main/not_found.html')


post_delete_view = login_required(PostDeleteView.as_view(), login_url="/login")


class PostUpdateView(UpdateView):
    def get(self, request, pk, *args, **kwargs):
        form = PostForm()
        profile = Profile.objects.get(user=request.user)

        try:
            post = Post.objects.get(pk=pk)
        except:
            return render(request, 'main/not_found.html')

        if not profile == post.author:
            messages.warning(request, 'You can only update your own posts.')

        context = {
            'form': form,
            'post': post
        }

        return render(request, 'posts/update.html', context)

    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)

        try:
            post = Post.objects.get(pk=pk)
        except:
            return render(request, 'main/not_found.html')

        if not profile == post.author:
            messages.warning(request, 'You can only update your own posts.')

        form = PostForm(request.POST, request.FILES)

        # Custom profanity words
        custom_badwords = CustomProfanity.objects.values_list(
            'bad_word', flat=True)
        profanity.load_censor_words(custom_badwords)

        valid = form.is_valid()

        if profanity.contains_profanity(form.cleaned_data.get('content')):
            custom_profanity_error = 'Please remove any profanity/swear words. (Added by an admin. Contact an admin if you believe this is wrong.)'
            valid = False
            form.errors['content'] = custom_profanity_error

        if valid:
            post.content = form.cleaned_data.get('content')
            if form.cleaned_data.get('image'):
                post.image = form.cleaned_data.get('image')
            post.save()
            return redirect(request.POST.get('referer'))

        context = {
            'form': form,
            'post': post
        }

        return render(request, 'posts/update.html', context)


post_update_view = login_required(PostUpdateView.as_view(), login_url="/login")


@login_required(login_url="/login")
def CommentDelete(request, pk):
    comment = Comment.objects.get(pk=pk)
    logged_user_profile = Profile.objects.get(user=request.user)
    if comment.user == logged_user_profile:
        comment.delete()

    return redirect('posts:posts-index')


class PostNotifications(View):
    def get(self, request, post_pk, *args, **kwargs):
        # notification = Notifications.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('posts:posts-index', pk=post_pk)


post_notifications = login_required(PostNotifications.as_view(), login_url="/login")


class FollowNotifications(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notifications.objects.get(pk=notification_pk)
        profile = Profile.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', pk=profile_pk)
        return redirect(request.headers.get('Referer'))


follow_notifications = login_required(FollowNotifications.as_view(), login_url="/login")


class ViewPost(View):
    def get(self, request, pk, *args, **kwargs):
        logged_in_user_profile = Profile.objects.get(user=request.user)
        form = CommentForm()

        try:
            post = Post.objects.get(pk=pk)

            context = {
                'profile': logged_in_user_profile,
                'post': post,
                'form': form
            }

            return render(request, 'posts/view_post.html', context)
        except:
            return render(request, 'main/not_found.html')

    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)

        # Custom profanity words
        custom_badwords = CustomProfanity.objects.values_list(
            'bad_word', flat=True)
        profanity.load_censor_words(custom_badwords)

        form = CommentForm(request.POST)

        valid = form.is_valid()

        if profanity.contains_profanity(form.cleaned_data.get('body')):
            custom_profanity_error = 'Please remove any profanity/swear words. (Added by an admin. Contact an admin if you believe this is wrong.)'
            valid = False
            form.errors['body'] = custom_profanity_error

        try:
            post = Post.objects.get(pk=pk)
        except:
            return redirect(request, 'main/not_found.html')

        if valid:
            comment_instance = form.save(commit=False)
            comment_instance.user = profile
            post = Post.objects.get(pk=pk)
            comment_instance.post = post
            comment_instance.save()

            notification = Notifications.objects.create(
                notification_type=2, from_user=request.user, to_user=post.author.user, post=post)

            return redirect(request.headers.get('Referer'))

        else:
            context = {
                'post': post,
                'profile': profile,
                'form': form
            }
            return render(request, 'posts/view_post.html', context)


view_post = login_required(ViewPost.as_view(), login_url="/login")
