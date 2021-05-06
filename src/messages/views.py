from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
from .models import Thread, Message
from profiles.models import Profile
from .forms import ThreadForm, MessageForm
from django.contrib.auth.decorators import login_required


# Create your views here.


class ListThreads(View):
    def get(self, request, *args, **kwargs):
        logged_in_user_profile = Profile.objects.get(user=request.user)
        threads = Thread.objects.filter(
            Q(user=logged_in_user_profile) |
            Q(receiver=logged_in_user_profile)
        )

        context = {
            'threads': threads,
            'profile': logged_in_user_profile
        }

        return render(request, 'messages/inbox.html', context)


list_threads = login_required(ListThreads.as_view(), login_url="/login")


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        logged_in_user_profile = Profile.objects.get(user=request.user)
        context = {
            'form': form,
            'profile': logged_in_user_profile
        }

        return render(request, 'messages/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        logged_in_user_profile = Profile.objects.get(user=request.user)
        username = request.POST.get('username')

        try:
            receiver_profile = Profile.objects.get(user__username=username)

            # Get only his friends so he can send messages to them
            friend_profiles = []
            friends = logged_in_user_profile.friends.all()
            for friend in friends:
                friend_profile = Profile.objects.get(user=friend)
                friend_profiles.append(friend_profile)

            if receiver_profile not in friend_profiles:
                return redirect('messages:create-thread')

            # Now we are sure that the user he's trying to message is in his friend list
            if Thread.objects.filter(user=logged_in_user_profile, receiver=receiver_profile).exists():
                thread = Thread.objects.filter(
                    user=logged_in_user_profile, receiver=receiver_profile)[0]
                return redirect('messages:thread', pk=thread.pk)
            elif Thread.objects.filter(user=receiver_profile, receiver=logged_in_user_profile).exists():
                thread = Thread.objects.filter(
                    user=receiver_profile, receiver=logged_in_user_profile)[0]
                return redirect('messages:thread', pk=thread.pk)

            if form.is_valid():
                thread = Thread(user=logged_in_user_profile,
                                receiver=receiver_profile)
                thread.save()
                return redirect('messages:thread', pk=thread.pk)
        except:
            return redirect('messages:create-thread')


create_thread = login_required(CreateThread.as_view(), login_url="/login")


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = Thread.objects.get(pk=pk)
        all_messages = Message.objects.filter(thread=thread)
        logged_in_user_profile = Profile.objects.get(user=request.user)

        context = {
            'thread': thread,
            'form': form,
            'messages': all_messages,
            'profile': logged_in_user_profile
        }

        return render(request, 'messages/thread.html', context)


thread_view = login_required(ThreadView.as_view(), login_url="/login")


class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        logged_in_user_profile = Profile.objects.get(user=request.user)
        thread = Thread.objects.get(pk=pk)

        if thread.receiver == logged_in_user_profile:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = Message(
            thread=thread,
            sender_profile=logged_in_user_profile,
            receiver_profile=receiver,
            body=request.POST.get('message')
        )

        message.save()

        return redirect('messages:thread', pk=pk)


create_message = login_required(CreateMessage.as_view(), login_url="/login")
