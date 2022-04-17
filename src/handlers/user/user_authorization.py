import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from config.loader import bot, cur, base
from data import text_data as td
from keyboards import inline as ik
from services.db import user as user_db

from states import UserAuth
from utils.number_validator import is_phone_number_valid

__all__ = [
    "user_authorization",
    "get_user_phone_number",
    "check_phone",
    "get_profile_panel"
]


async def get_profile_panel(message: types.Message):
    user_id = message.from_user.id
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    try:
        number = cur.execute('SELECT number FROM data WHERE id == ?', (message.from_user.id,)).fetchone()[0]
        if number:
            await bot.send_message(
                chat_id=user_id,
                text=td.SUCCESS_LOGIN,
                reply_markup=await ik.user_questions()
            )
    except Exception as e:
        await bot.send_message(
            chat_id=user_id,
            text=td.AUTHORIZATION,
            reply_markup=await ik.user_auth()
        )


async def user_authorization(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(chat_id=message.chat.id, text=td.AUTHORIZATION, reply_markup=await ik.user_auth())


async def get_user_phone_number(call: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=td.GET_USER_PHONE)
    await UserAuth.waiting_for_valid_phone.set()


async def check_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    phone_number = message.text
    if await is_phone_number_valid(phone_number):
        await state.finish()
        r = requests.get('https://api.nutritionscience.pro/api/v1/users/tgbot',
                         params={'phone': "89867178660"})  # params={'phone': "phone_number"}
        try:
            user = await user_db.select_user(user_id)
            if user:
                await bot.delete_message(
                    chat_id=user_id,
                    message_id=message.message_id
                )
                await bot.send_message(
                    chat_id=user_id,
                    text=td.AGAIN_AUTHORIZATED,
                    reply_markup=await ik.user_questions()
                )
                return
        except Exception as e:
            print("smt_here")
            pass
        user = await user_db.add_user(user_id, message.from_user.first_name)
        result = dict(r.json())
        await _role_segregated_menu(message, result, user)
    else:
        await bot.send_message(
            chat_id=user_id,
            text=td.INVALID_PHONE
        )


async def _role_segregated_menu(message: types.Message, result, user_type):
    user_id = message.from_user.id
    if result['user'] and not result['is_active']:
        await bot.send_message(
            chat_id=user_id,
            text=td.UNAVALIABLE_AUTH,
            reply_markup=await ik.user_auth()
        )
    if result['user'] and result['is_active']:
        if user_type == 'ученик':
            cur.execute('UPDATE data SET state == ? WHERE id == ?',
                        (1, message.from_user.id))
            base.commit()
            await bot.send_message(
                chat_id=user_id,
                text=td.SUCCESS_LOGIN,
                reply_markup=await ik.user_questions()
            )
        if user_type == 'куратор':
            cur.execute('UPDATE data SET state == ? WHERE id == ?',
                        (1, message.from_user.id))
            base.commit()
            await bot.send_message(
                chat_id=user_id,
                text=td.SUCCESS_LOGIN,
                reply_markup=await ik.main_kurator_menu()
            )
        if user_type == 'наставник':
            cur.execute('UPDATE data SET state == ? WHERE id == ?',
                        (1, message.from_user.id))
            base.commit()
            await bot.send_message(
                chat_id=user_id,
                text=td.SUCCESS_LOGIN,
                reply_markup=await ik.main_nastavnik_menu()
            )
    if not result['user'] and not result['is_active']:
        await bot.send_message(
            chat_id=message.chat.id,
            text=td.UNAVALIABLE_AUTH_2,
            reply_markup=ik.user_auth()
        )
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
