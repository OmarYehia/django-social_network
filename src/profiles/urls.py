from django.urls import path
from . import views
urlpatterns = [
    path("profile_view", views.profile_view, name="profile-view"),

]