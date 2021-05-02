from django.urls import path
from .views import posts_index, like_unlike_post


app_name = 'posts'

urlpatterns = [
    path('', posts_index, name='posts-index'),
    path('like/', like_unlike_post, name="like-unlike")
]
