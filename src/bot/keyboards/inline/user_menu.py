from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.data import keyboards_data as kd

__all__ = ["user_auth", "user_questions", "main_kurator_menu", "main_nastavnik_menu"]


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
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(
            text=kd.AUTHORIZATION_TXT, callback_data=kd.AUTHORIZATION_CD
        ),
        InlineKeyboardButton(
            text=kd.PROFILE_PANEL_TXT, callback_data=kd.PROFILE_PANEL_CD
        ),
        InlineKeyboardButton(
            text=kd.QUESTIONS_LIST_TXT, callback_data=kd.QUESTIONS_LIST_CD
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
            text=kd.AUTHORIZATION_TXT, callback_data=kd.AUTHORIZATION_CD
        ),
        InlineKeyboardButton(
            text=kd.PROFILE_PANEL_TXT, callback_data=kd.PROFILE_PANEL_CD
        ),
        InlineKeyboardButton(
            text=kd.QUESTIONS_LIST_TXT, callback_data=kd.QUESTIONS_LIST_CD
        ),
    )
    return keyboard
