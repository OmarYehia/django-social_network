from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from django.contrib.auth.models import User
from .forms import ProfileModelForm
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q


@login_required(login_url="/login")
def invites_received_view(request, slug):
    profile = Profile.objects.get(slug=slug)
    qs = Relationship.objects.invitaions_received(profile)
    result = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(result) == 0:
        is_empty = True

    context = {
        'qs': result,
        'is_empty': is_empty
    }
    print(is_empty)
    return render(request, 'profiles/my_invites.html', context)


@login_required(login_url="/login")
def accept_invitation(request, slug):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('/posts')


@login_required(login_url="/login")
def reject_invitation(request, slug):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('/posts')


@login_required(login_url="/login")
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


@login_required(login_url="/login")
def profiles_detail_view(request, slug):
    user = Profile.objects.get(user=request.user)
    profile = Profile.objects.get(slug=slug)
    rel_r = Relationship.objects.filter(sender=user)
    rel_s = Relationship.objects.filter(receiver=user)
    rel_receiver = []
    rel_sender = []
    for item in rel_r:
        rel_receiver.append(item.receiver.user)
    for item in rel_s:
        rel_sender.append(item.sender.user)
    posts = profile.get_all_author_posts
    print(request.user)
    is_empty = False
    if len(posts) == 0:
        is_empty = True

    context = {
        'user': user,
        'profile': profile,
        'posts': posts,
        'rel_sender': rel_sender,
        'rel_receiver': rel_receiver,
        'is_empty': is_empty
    }
    return render(request, 'profiles/detail.html', context)


@login_required(login_url="/login")
def invite_profiles_list_view(request, slug):
    user = User.objects.get(username=slug)
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'qs': qs
    }
    return render(request, 'profiles/to_invite_list.html', context)


@login_required(login_url="/login")
def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('/posts')


@login_required(login_url="/login")
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


profile_update_view = login_required(ProfileUpdateView.as_view(), login_url="/login")
