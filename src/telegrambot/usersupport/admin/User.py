from django.contrib import admin

from ..models import TelegramUser


class UsersAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")


# Register your models here.
admin.site.register(TelegramUser, UsersAdmin)
