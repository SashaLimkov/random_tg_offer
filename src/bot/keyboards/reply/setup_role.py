from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

break_role_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
break_btn = KeyboardButton(text="Отмена")
break_role_keyboard.row(break_btn)
