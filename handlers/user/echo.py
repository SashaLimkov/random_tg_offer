from aiogram import types

from config.loader import bot


async def echo_message(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=message.text)
