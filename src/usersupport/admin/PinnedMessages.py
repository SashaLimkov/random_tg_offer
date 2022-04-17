from django.contrib import admin

from ..models import PinnedMessage


class PinnedMessAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "kurators_chat", "mentors_chat")


# Register your models here.
admin.site.register(PinnedMessage, PinnedMessAdmin)
