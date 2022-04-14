from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import keyboards_data as kd

__all__ = [
    "is_question_right"
]


async def is_question_right():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text=kd.RIGHT_QUESTION_TXT, callback_data=kd.RIGHT_QUESTION_CD),
        InlineKeyboardButton(text=kd.WRONG_QUESTION_TXT, callback_data=kd.WRONG_QUESTION_CD)
    )
    return keyboard
