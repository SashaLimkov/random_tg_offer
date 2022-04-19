from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

__all__ = ["stop_keyboard", "no_comment_keyboard"]
stop_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
stop_btn = KeyboardButton(text="Завершить")
stop_keyboard.row(stop_btn)

no_comment_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
no_com_btn = KeyboardButton(text="Не оставлять отзыв")
no_comment_keyboard.row(no_com_btn)
