from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.data import keyboards_data as kd
from bot.services.db import question as question_db

__all__ = [
    "is_question_right",
    "is_get_answer",
    "is_new_question_right",
    "get_q_list",
    "answer_done",
    "back_to_q_list"
]

from usersupport.models import TelegramUser, UserQuestion


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


async def is_new_question_right():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=kd.RIGHT_QUESTION_TXT, callback_data=kd.NEW_RIGHT_QUESTION_CD
        ),
        InlineKeyboardButton(
            text=kd.WRONG_QUESTION_TXT, callback_data=kd.NEW_WRONG_QUESTION_CD
        ),
    )
    return keyboard


async def is_get_answer():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=kd.APPEND_QUESTION_TXT, callback_data=kd.ASK_A_QUESTION_CD
        ),
        InlineKeyboardButton(text=kd.ANSWER_DONE_TXT, callback_data=kd.ANSWER_DONE_CD),
    )
    return keyboard


async def answer_done():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text=kd.ANSWER_DONE_TXT, callback_data=kd.ANSWER_DONE_CD),
    )
    return keyboard


async def get_q_list(user):
    keyboard = InlineKeyboardMarkup(row_width=1)
    questions = await question_db.all_q(user)
    for question in questions[:18]:
        quid = question.pk
        q = question.question
        keyboard.add(InlineKeyboardButton(text=q, callback_data=f"quid_{quid}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back"))
    return keyboard


async def back_to_q_list():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(
        text="Назад", callback_data=kd.QUESTIONS_LIST_CD
    ))
    return keyboard
