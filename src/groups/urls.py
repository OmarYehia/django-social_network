from django.urls import path
from .views import ListGroups, CreateGroup, ViewGroup, JoinGroup, DeleteGroup, ViewGroupMembers, RemoveMember

app_name = 'groups'

urlpatterns = [
    path('', ListGroups.as_view(), name="groups-index"),
    path('create/', CreateGroup.as_view(), name="create-group"),
    path('<int:pk>/', ViewGroup.as_view(), name="view-group"),
    path('<int:pk>/join', JoinGroup.as_view(), name="join-group"),
    path('<int:pk>/delete', DeleteGroup.as_view(), name='delete-group'),
    path('<int:pk>/members', ViewGroupMembers.as_view(), name='group-members'),
    path('<int:pk>/members/<int:id>/delete',
         RemoveMember.as_view(), name='delete-member-group')
]