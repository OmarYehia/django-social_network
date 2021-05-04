from django.contrib import admin
from .models import Group
# Register your models here.


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'overview', 'created_at')


admin.site.register(Group, GroupAdmin)
