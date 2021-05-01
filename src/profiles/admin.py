from django.contrib import admin
from .models import Profile

# Register your models here.
<<<<<<< HEAD


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_total_posts', 'get_total_likes_given_number',
                    'get_total_likes_recieved_number', 'updated', 'created')


admin.site.register(Profile, ProfileAdmin)
=======
admin.site.register(Profile)
>>>>>>> ccf6936d24cac371e5c6c81931f5f24a2fe8a71c
