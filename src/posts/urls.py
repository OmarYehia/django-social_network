from django.urls import path
from . import views

urlpatterns = [
    path('posts-view', views.posts_view, name="posts-view"),

]
