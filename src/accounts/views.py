from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this


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


def login(request):
    form = AuthenticationForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            #return redirect()
        else:
            messages.error(request, "Invalid username or password.")
    else:
        messages.error(request, "Invalid username or password.")

    return render(request, "registration/login.html", {
        "form": form
    })


