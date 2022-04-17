from telegrambot.usersupport.models import TelegramUser
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(user_id)->TelegramUser:
    user = TelegramUser.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def add_user(user_id, name):
    try:
        return TelegramUser(
            user_id=int(user_id),
            name=name
        ).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def select_all_users():
    users = TelegramUser.objects.all()
    return users
