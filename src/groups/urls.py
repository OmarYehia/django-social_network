from django.urls import path
from .views import ListGroups, CreateGroup, ViewGroup, JoinGroup

app_name = 'groups'

urlpatterns = [
    path('', ListGroups.as_view(), name="groups-index"),
    path('create/', CreateGroup.as_view(), name="create-group"),
    path('<int:pk>/', ViewGroup.as_view(), name="view-group"),
    path('<int:pk>/join', JoinGroup.as_view(), name="join-group")
]
