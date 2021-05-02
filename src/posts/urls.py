from django.urls import path
from .views import posts_index, like_unlike_post, PostDeleteView, PostUpdateView


app_name = 'posts'

urlpatterns = [
    path('', posts_index, name='posts-index'),
    path('like/', like_unlike_post, name="like-unlike"),
    path('<pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('<pk>/update/', PostUpdateView.as_view(), name="post-update"),
]
