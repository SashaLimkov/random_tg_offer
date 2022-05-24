from django.db import models


# Create your models here.
class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class TelegramUser(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, verbose_name="UserID")
    name = models.CharField(max_length=255, verbose_name="UserName")
    user_role = models.CharField(max_length=255, verbose_name="Роль")
    state = models.IntegerField(verbose_name="Работает?", default=1)
    phone = models.CharField(max_length=12, unique=True)
    chat_id = models.BigIntegerField(verbose_name="Чат пользователя", default=0)
    chanel_id = models.BigIntegerField(verbose_name="Канал пользователя", default=0)


class UserQuestion(TimeBasedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    helper_id = models.BigIntegerField(
        unique=False, verbose_name="ID Отвечающего", default=0
    )
    question = models.CharField(max_length=5000, verbose_name="Вопрос")
    history = models.CharField(
        max_length=10000, verbose_name="История вопроса", null=True
    )
    history2 = models.CharField(
        max_length=10000, verbose_name="История вопроса с временем", null=True
    )
    state = models.CharField(
        max_length=100, verbose_name="Состояние", default="Открытый вопрос"
    )
    rate = models.CharField(max_length=1, verbose_name="Оценка", null=True)
    feedback = models.CharField(max_length=5000, null=True)
    mes_id = models.CharField(max_length=20000, unique=False, default="")


class PinnedMessage(TimeBasedModel):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(UserQuestion, on_delete=models.DO_NOTHING)
    kurators_chat = models.BigIntegerField(verbose_name="id вопроса у кураторов")
    mentors_chat = models.BigIntegerField(verbose_name="id вопроса у наставников")
