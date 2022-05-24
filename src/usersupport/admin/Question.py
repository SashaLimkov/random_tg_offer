from django.contrib import admin

from ..models import UserQuestion


class QuestionsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "helper_id",
        "question",
        "history",
        "history2",
        "state",
        "rate",
        "feedback",
        "created_at",
        "updated_at",
    )


# Register your models here.
admin.site.register(UserQuestion, QuestionsAdmin)
