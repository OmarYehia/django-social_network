from django.urls import path
from .views import list_groups, create_group, view_group, join_group, delete_group, view_group_members, remove_member

app_name = 'groups'

urlpatterns = [
    path('', list_groups, name="groups-index"),
    path('create/', create_group, name="create-group"),
    path('<int:pk>/', view_group, name="view-group"),
    path('<int:pk>/join', join_group, name="join-group"),
    path('<int:pk>/delete', delete_group, name='delete-group'),
    path('<int:pk>/members', view_group_members, name='group-members'),
    path('<int:pk>/members/<int:id>/delete',
         remove_member, name='delete-member-group')
]
