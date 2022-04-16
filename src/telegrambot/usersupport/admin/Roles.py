from django.contrib import admin

from ..models import Role


class UsersRolesAdmin(admin.ModelAdmin):
    list_display = ("t_user", "user_role", "created_at")


# Register your models here.
admin.site.register(Role, UsersRolesAdmin)
