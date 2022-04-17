from usersupport.models import TelegramUser
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(user_id) -> TelegramUser:
    user = TelegramUser.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def add_user(user_id, name, role, phone_number):
    try:
        return TelegramUser(
            user_id=int(user_id),
            name=name,
            user_role=role,
            phone=phone_number
        ).save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def update_user_phone(user_id, phone):
    return TelegramUser.objects.filter(user_id=user_id).update(phone=phone)


@sync_to_async
def update_user_state(user_id, state):
    return TelegramUser.objects.filter(user_id=user_id).update(state=state)


@sync_to_async
def select_all_users():
    users = TelegramUser.objects.all()
    return users


@sync_to_async
def select_all_kurators_and_mentors():
    kurators = TelegramUser.objects.filter(user_role="куратор").all()
    mentors = TelegramUser.objects.filter(user_role="настваник").all()
    return kurators, mentors


@sync_to_async
def get_user_by_chanel_chat_id(chat_id):
    user = TelegramUser.objects.filter(chat_id=chat_id).first()
    return user


@sync_to_async
def update_chanel_chat_id(user_id, chat_id):
    return TelegramUser.objects.filter(user_id=user_id).update(chat_id=chat_id)


@sync_to_async
def update_chanel_id(user_id, chanel_id):
    return TelegramUser.objects.filter(user_id=user_id).update(chanel_id=chanel_id)
