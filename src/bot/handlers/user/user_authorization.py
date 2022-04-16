import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from src.bot.config.loader import bot, cur, base
from src.bot.data import text_data as td
from src.bot.keyboards import inline as ik

from src.bot.states import UserAuth
from src.bot.utils.number_validator import is_phone_number_valid

__all__ = [
    "user_authorization",
    "get_user_phone_number",
    "check_phone",
    "get_profile_panel"
]


async def get_profile_panel(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    try:
        number = cur.execute('SELECT number FROM data WHERE id == ?', (message.from_user.id,)).fetchone()[0]
        if number:
            await bot.send_message(chat_id=message.chat.id, text=td.SUCCESS_LOGIN,
                                   reply_markup=await ik.user_questions())
    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text=td.AUTHORIZATION, reply_markup=await ik.user_auth())


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
    phone_number = message.text
    if await is_phone_number_valid(phone_number):
        await state.finish()
        r = requests.get('https://api.nutritionscience.pro/api/v1/users/tgbot',
                         params={'phone': "89867178660"})  # params={'phone': "phone_number"}
        try:
            authorizted = cur.execute('SELECT state FROM data WHERE id = ?', (message.from_user.id,)).fetchone()[0]
            if authorizted == 1:
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id
                )
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=td.AGAIN_AUTHORIZATED,
                    reply_markup=await ik.user_questions()
                )
                return
        except Exception as e:
            print(e)
        cur.execute('INSERT INTO  data VALUES(?,?,?,?,?)',
                    (message.from_user.id, phone_number, 'ученик', '0', '0'))
        base.commit()
        user_type = cur.execute('SELECT role FROM data WHERE id = ?', (message.from_user.id,)).fetchone()[0]
        result = dict(r.json())
        await _role_segregated_menu(message, result, user_type)
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=td.INVALID_PHONE
        )


async def _role_segregated_menu(message: types.Message, result, user_type):
    if result['user'] and not result['is_active']:
        await bot.send_message(
            chat_id=message.chat.id,
            text=td.UNAVALIABLE_AUTH,
            reply_markup=await ik.user_auth()
        )
    if result['user'] and result['is_active']:
        if user_type == 'ученик':
            cur.execute('UPDATE data SET state == ? WHERE id == ?',
                        (1, message.from_user.id))
            base.commit()
            await bot.send_message(
                chat_id=message.chat.id,
                text=td.SUCCESS_LOGIN,
                reply_markup=await ik.user_questions()
            )
        if user_type == 'куратор':
            cur.execute('UPDATE data SET state == ? WHERE id == ?',
                        (1, message.from_user.id))
            base.commit()
            await bot.send_message(
                chat_id=message.chat.id,
                text=td.SUCCESS_LOGIN,
                reply_markup=await ik.main_kurator_menu()
            )
        if user_type == 'наставник':
            cur.execute('UPDATE data SET state == ? WHERE id == ?',
                        (1, message.from_user.id))
            base.commit()
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
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
