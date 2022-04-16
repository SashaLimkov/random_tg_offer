from asgiref.sync import sync_to_async

from usersupport import models


@sync_to_async
def add_user(
    chat_id,
):
    chat = models.ModeratedChat.objects.filter(chat_id=chat_id).first()
    return chat
