from django.shortcuts import render, redirect
from django.views import View
from .models import Group
from .forms import GroupForm
from profiles.models import Profile
from posts.models import Post
from posts.forms import PostForm, CommentForm

# Create your views here.


class ListGroups(View):
    def get(self, request, *args, **kwargs):
        logged_in_user_profile = Profile.objects.get(user=request.user)

        groups = Group.objects.all()

        context = {
            'groups': groups,
            'profile': logged_in_user_profile
        }

        return render(request, 'groups/groups.html', context)


class CreateGroup(View):
    def get(self, request, *args, **kwargs):
        form = GroupForm()

        context = {
            'form': form,
        }

        return render(request, 'groups/create.html', context)

    def post(self, request, *args, **kwargs):
        form = GroupForm(request.POST)
        logged_in_user_profile = Profile.objects.get(user=request.user)

        if form.is_valid():
            group_instance = form.save(commit=False)
            group_instance.owner = logged_in_user_profile
            group_instance.save()
            group_instance.users.add(logged_in_user_profile)

            return redirect('groups:view-group', pk=group_instance.pk)

        return render(request, 'groups/create.html', {'form': form})


class ViewGroup(View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        group = Group.objects.get(pk=pk)

        if not profile in group.users.all():
            return redirect('groups:groups-index')

        group_posts = Post.objects.filter(group=group)

        context = {
            'profile': profile,
            'group': group,
            'posts': group_posts
        }

        return render(request, 'groups/view.html', context)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        group = Group.objects.get(pk=pk)

        if 'submit_post_form' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post_instance = post_form.save(commit=False)
                post_instance.author = profile
                post_instance.group = group
                post_instance.save()
                return redirect(request.headers.get('Referer'))

        elif 'submit_comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                post_id = request.POST.get("post_id")
                comment_instance = comment_form.save(commit=False)
                comment_instance.user = profile
                comment_instance.post = Post.objects.get(id=post_id)
                comment_instance.save()
                return redirect(request.headers.get('Referer'))


class JoinGroup(View):
    def get(self, request, pk, *args, **kwargs):
        group = Group.objects.get(pk=pk)
        user = request.user
        user_profile = Profile.objects.get(user=user)

        if user_profile in group.users.all():
            return redirect('groups:view-group', pk=pk)

        return render(request, 'groups/confirm_join.html', {'group': group})

    def post(self, request, pk, *args, **kwargs):
        group = Group.objects.get(pk=pk)
        user = request.user
        user_profile = Profile.objects.get(user=user)

        group.users.add(user_profile)

        return redirect('groups:view-group', pk=pk)


class DeleteGroup(View):
    def get(self, request, pk, *args, **kwargs):
        group = Group.objects.get(pk=pk)
        user = request.user
        user_profile = Profile.objects.get(user=user)

        if not user_profile == group.owner:
            return redirect('groups:view-group', pk=pk)

        return render(request, 'groups/confirm_delete.html', {'group': group})

    def post(self, request, pk, *args, **kwargs):
        group = Group.objects.get(pk=pk)
        user = request.user
        user_profile = Profile.objects.get(user=user)

        if not user_profile == group.owner:
            return redirect('groups:view-group', pk=pk)

        group.delete()

        return redirect('groups:groups-index')
