from django.shortcuts import render
from .models import Profile
from django.views.generic import TemplateView, View
from django.http import JsonResponse


# Create your views here.
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profiles/view.html', {'profile': profile})


class MyProfileView(TemplateView):
    template_name = 'profiles/my_profile.html'


class MyProfileData(View):
    def get(self, *args, **kwargs):
        profile = Profile.object.get(user=self.request.user)
        qs = profile.get_proposals_for_following()
        profiles_to_follow_list = []
        for user in qs:
            profile = Profile.objects.get(user__username=user.username)
            profile_item = {
                'id': profile.id,
                "user": profile.user.username,
                'avatar': profile.avatar.url,
            }
            profiles_to_follow_list.append(profile_item)
        return JsonResponse({'profile_data': profiles_to_follow_list})
