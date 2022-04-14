import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from config.loader import bot
from data import text_data as td
from keyboards.inline.user_menu import user_auth

__all__ = [
    "user_authorization",
    "get_user_phone_number",
    "check_phone"
]

from states import UserAuth
from utils.number_validator import is_phone_number_valid


async def user_authorization(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=td.AUTHORIZATION, reply_markup=await user_auth())


async def get_user_phone_number(call: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=td.GET_USER_PHONE)
    await UserAuth.waiting_for_valid_phone.set()


async def check_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    if await is_phone_number_valid(phone_number):
        await state.finish()
        r = requests.get('https://api.nutritionscience.pro/api/v1/users/tgbot',
                         params={'phone': "89867178660"})  # params={'phone': "phone_number"}

        result = dict(r.json())
        if result['user'] == True and result['is_active'] == False:
            await bot.send_message(id, "Учетная запись неактивна, либо не приобретен курс. Отправить вопрос невозможно",
                                   reply_markup=kb.main)
        if result['user'] == True and result['is_active'] == True:
            if type == 'ученик':
                await bot.send_message(id, "Вы успешно авторизовались", reply_markup=kb.ask)
            if type == 'куратор':
                await bot.send_message(id, "Вы успешно авторизовались", reply_markup=kb.mainkur)
            if type == 'наставник':
                await bot.send_message(id, "Вы успешно авторизовались", reply_markup=kb.mainknast)
        if result['user'] == False and result['is_active'] == False:
            await bot.send_message(id, "Авторизация невозможна.", reply_markup=kb.main)
        await bot.send_message(
            chat_id=message.chat.id,
            text=result
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=td.INVALID_PHONE
        )
