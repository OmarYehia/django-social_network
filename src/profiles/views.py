from django.shortcuts import render
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import NewUserForm, ProfileUpdateForm


# Create your views here.

def signup(request):
    form = NewUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
    return render(request, "registration/signup.html", {
        "form": form
    })


@login_required
def profile(request):
    form = ProfileUpdateForm(request.POST, instance=request.user.profile or None)
    if  form.is_valid():
        form.save()
       # return redirect('profile')

     context = {
        'form': form
    }

    #return render(request, 'profiles/profile.html', context)


@login_required(login_url="/login")
def my_profile_view(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    context = {
        'profile': profile,
    }
    return render(request, 'profiles/myprofile.html', context)

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
