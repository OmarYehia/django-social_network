from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path("<slug>", views.profiles_detail_view, name="my-profile-view"),
    path('<slug>/update/', views.profile_update_view , name="profile-update"),
    path('<slug>/my-invites/', views.invites_received_view, name='my-invites-view'),
    path('<slug>/all-profiles/', views.profiles_list_view, name='all-profiles-view'),
    path('<slug>/to-invite/', views.invite_profiles_list_view, name='to-invite-view'),
    path('send-invite/', views.send_invitation, name='send-invitation'),
    path('remove-friend/', views.remove_from_fiends, name='remove-friend'),
    path('<slug>/my-invites/accept', views.accept_invitation, name='accept-invite'),
    path('<slug>/my-invites/reject', views.reject_invitation, name='reject-invite'),

]
