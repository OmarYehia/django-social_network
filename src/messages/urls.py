from django.urls import path
from .views import ListThreads, CreateThread, ThreadView, CreateMessage


app_name = 'messages'

urlpatterns = [
    path('', ListThreads.as_view(), name='inbox'),
    path('create-thread/', CreateThread.as_view(), name='create-thread'),
    path('<int:pk>/', ThreadView.as_view(), name='thread'),
    path('<int:pk>/create-message/', CreateMessage.as_view(), name='create-message')
]
