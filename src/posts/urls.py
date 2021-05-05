from django.urls import path
from .views import posts_index, like_unlike_post, PostDeleteView, PostUpdateView, CommentDelete, ViewPost


app_name = 'posts'

urlpatterns = [
    path('', posts_index, name='posts-index'),
    path('like/', like_unlike_post, name="like-unlike"),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('<int:pk>/delete-comment/', CommentDelete, name="comment-delete"),
    path('<int:pk>/', ViewPost.as_view(), name='view-post')
]
