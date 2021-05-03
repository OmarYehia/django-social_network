from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path("<str:username>", views.my_profile_view, name="my-profile-view"),
    path('<slug>/update/', views.ProfileUpdateView.as_view(), name="profile-update"),
    path('<slug>/my-invites/', views.invites_received_view, name='my-invites-view'),
    path('<slug>/all-profiles/', views.profiles_list_view, name='all-profiles-view'),

    #path('my/', views.my_profile_view, name='my-profile-view'),
    #path('my-profile-json/', views.MyProfileData.as_view(), name='my-profile-json')

]
