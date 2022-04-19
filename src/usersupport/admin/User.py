from django.contrib import admin

from ..models import TelegramUser


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "user_id",
        "user_role",
        "state",
        "chanel_id",
        "chat_id",
        "created_at",
        "updated_at",
    )


# Register your models here.
admin.site.register(TelegramUser, UsersAdmin)
