from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.bot.data import keyboards_data as kd

__all__ = ["is_question_right", "is_get_answer"]


async def is_question_right():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=kd.RIGHT_QUESTION_TXT, callback_data=kd.RIGHT_QUESTION_CD
        ),
        InlineKeyboardButton(
            text=kd.WRONG_QUESTION_TXT, callback_data=kd.WRONG_QUESTION_CD
        ),
    )
    return keyboard


async def is_get_answer():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=kd.APPEND_QUESTION_TXT, callback_data=kd.APPEND_QUESTION_CD
        ),
        InlineKeyboardButton(text=kd.ANSWER_DONE_TXT, callback_data=kd.ANSWER_DONE_CD),
    )
    return keyboard
