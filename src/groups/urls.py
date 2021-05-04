from django.urls import path
from .views import ListGroups, CreateGroup

app_name = 'groups'

urlpatterns = [
    path('', ListGroups.as_view(), name="groups-index"),
    path('create/', CreateGroup.as_view(), name="create-group")
]
