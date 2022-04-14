import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from config.loader import bot
from data import text_data as td
from keyboards import inline as ik

__all__ = [
    "user_authorization",
    "get_user_phone_number",
    "check_phone"
]

from states import UserAuth
from utils.number_validator import is_phone_number_valid


async def user_authorization(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=td.AUTHORIZATION, reply_markup=await ik.user_auth())


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
        user_type = ...  # получаем тип юзера из бд по номеру, как я понял
        result = dict(r.json())
        if result['user'] and not result['is_active']:
            await bot.send_message(
                chat_id=message.chat.id,
                text=td.UNAVALIABLE_AUTH,
                reply_markup=await ik.user_auth()
            )
        if result['user'] and result['is_active']:
            if user_type == 'ученик':
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=td.SUCCESS_LOGIN,
                    reply_markup=await ik.user_questions()
                )
            if user_type == 'куратор':
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=td.SUCCESS_LOGIN,
                    reply_markup=await ik.main_kurator_menu()
                )
            if user_type == 'наставник':
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=td.SUCCESS_LOGIN,
                    reply_markup=await ik.main_nastavnik_menu()
                )
        if not result['user'] and not result['is_active']:
            await bot.send_message(
                chat_id=message.chat.id,
                text=td.UNAVALIABLE_AUTH_2,
                reply_markup=ik.user_auth()
            )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=td.INVALID_PHONE
        )
