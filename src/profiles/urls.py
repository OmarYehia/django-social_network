from django.urls import path
from . import views

urlpatterns = [
    path("profile-view", views.profile_view, name="profile-view"),
    path('my/', views.MyProfileView.as_view(), name='my-profile-view'),
    path('my-profile-json/', views.MyProfileData.as_view(), name='my-profile-json')

]
