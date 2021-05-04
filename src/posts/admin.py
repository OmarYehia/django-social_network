from django.contrib import admin
from .models import Post, Comment, Like, Notifications
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'get_total_likes',
                    'get_total_comments', 'updated_at', 'created_at')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'updated_at', 'created_at')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'value', 'updated_at', 'created_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Notifications)