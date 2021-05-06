from django.urls import path
from .views import list_threads, create_thread, thread_view, create_message


app_name = 'messages'

urlpatterns = [
    path('', list_threads, name='inbox'),
    path('create-thread/', create_thread, name='create-thread'),
    path('<int:pk>/', thread_view, name='thread'),
    path('<int:pk>/create-message/', create_message, name='create-message')
]
