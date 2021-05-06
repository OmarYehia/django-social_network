from django.urls import path
from .views import posts_index, like_unlike_post, post_delete_view, post_update_view, CommentDelete, post_notifications, follow_notifications, view_post


app_name = 'posts'

urlpatterns = [
    path('', posts_index, name='posts-index'),
    path('like/', like_unlike_post, name="like-unlike"),
    path('<int:pk>/delete/', post_delete_view, name="post-delete"),
    path('<int:pk>/update/', post_update_view, name="post-update"),
    path('<int:pk>/delete-comment/', CommentDelete, name="comment-delete"),
    path('<int:post_pk>', post_notifications, name="post-notification"),
    path('notification/<int:notification_pk>/profile/<int:profile_pk>', follow_notifications, name="follow-notification"),
    path('<int:pk>/', view_post, name='view-post')
]
