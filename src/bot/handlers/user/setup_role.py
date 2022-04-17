from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.config.config import KURATOR_SECRET_KEY, NASTAVNIK_SECRET_KEY
from bot.config.loader import bot
from bot.keyboards.reply.setup_role import break_role_keyboard
from bot.states.setup_role import Role
from bot.services.db import user as user_db
from usersupport import models


async def setup_user_role(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Введите секретный ключ",
        reply_markup=break_role_keyboard
    )
    await Role.secret_key.set()


async def check_key(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    secret_key = message.text
    if secret_key == KURATOR_SECRET_KEY:
        user: models.TelegramUser = await user_db.add_user(user_id=user_id, name=message.from_user.first_name,
                                                           role="куратор", phone_number=".")
        await state.finish()
        await bot.send_message(
            chat_id=user_id,
            text=f"Вы успешно авторизированы как куратор",
            reply_markup=ReplyKeyboardRemove()
        )
    elif secret_key == NASTAVNIK_SECRET_KEY:
        user = await user_db.add_user(user_id=user_id, name=message.from_user.first_name,
                                      role="наставник", phone_nuber=".")
        await state.finish()
        await bot.send_message(
            chat_id=user_id,
            text=f"Вы успешно авторизированы как наставник",
            reply_markup=ReplyKeyboardRemove()
        )
    elif secret_key == "Отмена":
        await state.finish()
        await bot.send_message(
            chat_id=user_id,
            text="Действия отменены",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text="Введенный ключ не соответсвует ни одной из ролей, попробуйте заново или нажмите на кнопку",
            reply_markup=break_role_keyboard
        )
