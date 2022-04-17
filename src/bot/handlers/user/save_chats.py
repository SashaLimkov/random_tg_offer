from aiogram import types
from bot.services.db import user as user_db
from usersupport.models import TelegramUser


async def update_chat_id(message: types.Message):
    user_id = message.left_chat_member.id
    kurators, mentors = await user_db.select_all_kurators_and_mentors()
    k_list = [k.user_id for k in kurators]
    m_list = [m.user_id for m in mentors]
    if user_id in k_list or user_id in m_list:
        await user_db.update_chanel_chat_id(user_id=user_id, chat_id=message.chat.id)


async def update_chanel(message: types.Message):
    if "forward_from_chat" in message:
        chat_id = message.chat.id
        chanel_id = message.forward_from_chat.id
        user: TelegramUser = await user_db.get_user_by_chanel_chat_id(chat_id=chat_id)
        await user_db.update_chanel_id(user_id=user.user_id, chanel_id=chanel_id)
