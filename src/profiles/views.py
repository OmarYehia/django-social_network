from django.shortcuts import render, redirect
from .models import Profile, Relationship
from django.contrib.auth.models import User
from .forms import ProfileModelForm
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q


@login_required(login_url="/login")
def my_profile_view(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    form = ProfileModelForm(request.POST or None,
                            request.FILES or None, instance=profile)
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
    user = User.objects.get(username=slug)
    qs = Profile.objects.get_all_profiles(user)
    profile = Profile.objects.get(user=user)
    rel_r = Relationship.objects.filter(sender=profile)
    rel_s = Relationship.objects.filter(receiver=profile)
    rel_receiver = []
    rel_sender = []
    for item in rel_r:
        rel_receiver.append(item.receiver.user)
    for item in rel_s:
        rel_sender.append(item.sender.user)
    is_empty = False
    if len(qs) == 0:
        is_empty = True

    context = {
        'qs': qs,
        'rel_sender': rel_sender,
        'rel_receiver': rel_receiver,
        'is_empty': is_empty
    }
    return render(request, 'profiles/profile_list.html', context)


def invite_profiles_list_view(request, slug):
    user = User.objects.get(username=slug)
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'qs': qs
    }
    return render(request, 'profiles/to_invite_list.html', context)


def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('/posts')


def remove_from_fiends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | Q(sender=receiver) & Q(receiver=sender)
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('/posts')



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
