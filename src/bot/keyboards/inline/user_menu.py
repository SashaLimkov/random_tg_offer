from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.data import keyboards_data as kd

__all__ = [
    "user_auth",
    "user_questions",
    "main_kurator_menu",
    "main_nastavnik_menu",
    "set_kurators_rate",
]


async def user_auth():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(
            text=kd.AUTHORIZATION_TXT, callback_data=kd.AUTHORIZATION_CD
        ),
    )
    return keyboard


async def user_questions():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=kd.ASK_A_QUESTION_TXT, callback_data=kd.ASK_A_QUESTION_CD
        ),
        InlineKeyboardButton(
            text=kd.QUESTIONS_LIST_TXT, callback_data=kd.QUESTIONS_LIST_CD
        ),
    )
    return keyboard


async def main_kurator_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=kd.QUESTIONS_LIST_TXT, callback_data="asdasd"
        ),
        InlineKeyboardButton(
            text=kd.KUR_ACTIVITY_TXT, callback_data=kd.KUR_ACTIVITY_CD
        ),
    )
    return keyboard


async def main_nastavnik_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(
            text=kd.QUESTIONS_LIST_TXT, callback_data="asdasd"
        ),
    )
    return keyboard


async def set_kurators_rate():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="1", callback_data="r_1"),
        InlineKeyboardButton(text="2", callback_data="r_2"),
        InlineKeyboardButton(text="3", callback_data="r_3"),
        InlineKeyboardButton(text="4", callback_data="r_4"),
        InlineKeyboardButton(text="5", callback_data="r_5"),
    )
    return keyboard
