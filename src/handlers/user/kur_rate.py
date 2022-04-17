from aiogram import types
from aiogram.types import ReplyKeyboardRemove

import config.config
from config.loader import bot
from keyboards import reply as rk
from states import Rate


async def set_rate(call: types.CallbackQuery):
    rate = int(call.data.replace("r_", ""))
    await bot.send_message(
        chat_id=config.config.CHANNEL_NASTAVNIK,
        text=f"Оценка от пользователя {rate}"
    )

    await Rate.waiting_for_rate.set()

    if rate <= 3:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Пожалуйста, напишите что вас не устроило",
            reply_markup=rk.no_comment_keyboard
        )


async def get_rate(message: types.Message):
    if message.text == "Не оставлять отзыв":
        await bot.send_message(chat_id=message.chat.id,text="Просто напишите /start, чтобы начать с начала",
                               reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(
            chat_id=config.config.CHANNEL_NASTAVNIK,
            text=f"Отзыв от пользователя:\n{message.text}"
        )
        await bot.send_message(chat_id=message.chat.id, text="Просто напишите /start, чтобы начать с начала",
                               reply_markup=ReplyKeyboardRemove())