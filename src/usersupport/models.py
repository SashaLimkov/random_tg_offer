from django.db import models


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class TelegramUser(TimeBasedModel):
    user_id = models.BigIntegerField(
        primary_key=True, unique=True, verbose_name="UserChatId"
    )
    name = models.CharField(max_length=255, verbose_name="UserName")


class Role(TelegramUser):
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.DO_NOTHING,
        verbose_name="Пользователь",
        related_name="User",
    )
    user_role = models.CharField(max_length=255, verbose_name="Роль")


class UserQuestion(TimeBasedModel):
    user = models.ForeignKey(
        TelegramUser, on_delete=models.DO_NOTHING, verbose_name="Пользователь"
    )
    question = models.CharField(max_length=4000, verbose_name="Вопрос")
    kurators_mes_id = models.BigIntegerField(verbose_name="id вопроса у кураторов")
    mentors_mes_id = models.BigIntegerField(verbose_name="id вопроса у наставников")
