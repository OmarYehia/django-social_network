from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import NewUserForm
#from django.contrib import messages
#from django.contrib.auth.forms import AuthenticationForm #add this


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




