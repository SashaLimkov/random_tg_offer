from aiogram import types
from bot.services.db import user as user_db


async def update_chanel(message: types.Message):
    chat_id = message.chat.id
    chanel_id = message.forward_from_chat.id
    await user_db.update_chanel_id(chat_id=chat_id, chanel_id=chanel_id)
