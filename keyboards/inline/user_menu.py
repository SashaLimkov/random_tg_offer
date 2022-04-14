from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import keyboards_data as kd


async def user_auth():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text='Авторизация', callback_data=kd.AUTHORIZATION),
    )
    return keyboard
