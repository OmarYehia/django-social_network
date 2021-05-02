from django.contrib import admin
from .models import Profile, Relationship

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_total_posts', 'get_total_likes_given_number',
                    'get_total_likes_recieved_number', 'updated', 'created')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Relationship)