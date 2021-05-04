from django.shortcuts import render, redirect


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'main/index.html', {})

    return redirect("posts:posts-index")
