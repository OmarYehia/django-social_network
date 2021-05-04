from django.shortcuts import render, redirect
from django.views import View
from .models import Group
from .forms import GroupForm
from profiles.models import Profile
from posts.models import Post

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
            group_instance.users.set([logged_in_user_profile])

            return redirect('groups:groups-index')

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
