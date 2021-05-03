from django.shortcuts import render, redirect
from .models import Profile, Relationship
from django.contrib.auth.models import User
from .forms import ProfileModelForm
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required


@login_required(login_url="/login")
def my_profile_view(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm
    }
    return render(request, 'profiles/myprofile.html', context)


def invites_received_view(request, slug):
    profile = Profile.objects.get(slug=slug)
    qs = Relationship.objects.invitaions_received(profile)

    context = {
        'qs': qs
    }
    return render(request, 'profiles/my_invites.html', context)


def profiles_list_view(request, slug):
    user = slug
    qs = Profile.objects.invitaions_received(user)

    context = {
        'qs': qs
    }
    return render(request, 'profiles/profile_list.html', context)


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileModelForm
    template_name = 'profiles/update.html'
    success_url = reverse_lazy('posts:posts-index')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        user = User.objects.get(username=self.request.user)
        if form.instance.user == profile.user:
            user.first_name = form.instance.first_name
            user.last_name = form.instance.last_name
            user.email = form.instance.email
            user.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'You can update only your own profile.')
            return super().form_invalid(form)

# @login_required(login_url="/login")
# class MyProfileView(TemplateView):
#    template_name = 'profiles/my_profile.html'


# my_profile_view = login_required(MyProfileView.as_view(),login_url="/login" )


# @login_required(login_url="/login")
# class MyProfileData(View):
#   def get(self, *args, **kwargs):
#      profile = Profile.objects.get(user=self.request.user)
#     qs = profile.get_proposals_for_following()
#     profiles_to_follow_list = []
#    for user in qs:
#       profile = Profile.objects.get(user__username=user.username)
#      profile_item = {
#         'id': profile.id,
#        "user": profile.user.username,
#       'avatar': profile.avatar.url,
#  }
# profiles_to_follow_list.append(profile_item)
# return JsonResponse({'profile_data': profiles_to_follow_list})
