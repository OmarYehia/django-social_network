from django.shortcuts import render, redirect
from django.views import View
from .models import Group
from .forms import GroupForm
from profiles.models import Profile
from posts.models import Post
from posts.forms import PostForm, CommentForm
from posts.models import CustomProfanity
from better_profanity import profanity

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

    def post(self, request, *args, **kwargs):
        form = GroupForm(request.POST)
        logged_in_user_profile = Profile.objects.get(user=request.user)

        if not form.is_valid():
            return redirect('groups:groups-index')

        group_name = form.cleaned_data.get('name')

        try:
            groups = Group.objects.filter(name__icontains=group_name)
            return render(request, 'groups/groups.html', {'groups': groups})
        except:
            return render(request, 'groups/groups.html')


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
        post_form = PostForm()
        comment_form = CommentForm()

        if not profile in group.users.all():
            return redirect('groups:groups-index')

        group_posts = Post.objects.filter(group=group)

        context = {
            'profile': profile,
            'group': group,
            'posts': group_posts,
            'post_form': post_form,
            'comment_form': comment_form
        }

        return render(request, 'groups/view.html', context)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        group = Group.objects.get(pk=pk)

        # Custom profanity words
        custom_badwords = CustomProfanity.objects.values_list(
            'bad_word', flat=True)
        profanity.load_censor_words(custom_badwords)

        if 'submit_post_form' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            comment_form = None
            valid = post_form.is_valid()

            if profanity.contains_profanity(post_form.cleaned_data.get('content')):
                custom_profanity_error = 'Please remove any profanity/swear words. (Added by an admin. Contact an admin if you believe this is wrong.)'
                valid = False
                post_form.errors['content'] = custom_profanity_error

            if valid:
                post_instance = post_form.save(commit=False)
                post_instance.author = profile
                post_instance.group = group
                post_instance.save()
                return redirect('groups:view-group', pk=pk)

        elif 'submit_comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            post_form = None
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
                return redirect(request.headers.get('Referer'))

        group_posts = Post.objects.filter(group=group)

        context = {
            'profile': profile,
            'group': group,
            'posts': group_posts,
            'post_form': post_form,
            'comment_form': comment_form
        }

        return render(request, 'groups/view.html', context)


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


class ViewGroupMembers(View):
    def get(self, request, pk, *args, **kwargs):
        group = Group.objects.get(pk=pk)
        group_members = group.users.all().exclude(user=group.owner.user)
        logged_in_user_profile = Profile.objects.get(user=request.user)

        context = {
            'members': group_members,
            'profile': logged_in_user_profile,
            'group': group
        }

        return render(request, 'groups/view_members.html', context)


class RemoveMember(View):
    def get(self, request, pk, id, *args, **kwargs):
        group = Group.objects.get(pk=pk)
        logged_in_user_profile = Profile.objects.get(user=request.user)
        try:
            member_to_delete = Profile.objects.get(pk=id)
            group_members = group.users.all().exclude(user=group.owner.user)

            if not logged_in_user_profile == group.owner or not member_to_delete in group_members:
                return redirect('groups:group-members', pk=group.pk)

            member_to_delete.groups.remove(group)
            return redirect('groups:group-members', pk=group.pk)
        except:
            return redirect('groups:group-members', pk=group.pk)
