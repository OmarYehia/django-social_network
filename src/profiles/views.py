from django.shortcuts import render
from .models import Profile


# Create your views here.
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profiles/view.html', {'profile': profile})
