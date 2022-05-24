import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot, mes_to_del
from bot.data import text_data as td
from bot.handlers.user.cleaner import del_mes_history
from bot.keyboards import inline as ik
from bot.services.db import user as user_db
from bot.states import UserAuth
from bot.utils.number_validator import is_phone_number_valid

__all__ = [
    "user_authorization",
    "get_user_phone_number",
    "check_phone",
    "get_profile_panel",
]

from usersupport.models import TelegramUser


async def get_profile_panel(message: types.Message):
    user_id = message.from_user.id
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    try:
        user: TelegramUser = await user_db.select_user(user_id=user_id)
        if user:
            await bot.send_message(
                chat_id=user_id,
                text=td.SUCCESS_LOGIN_USR.format(user.name),
                reply_markup=await ik.user_questions(),
            )
    except Exception:
        await bot.send_message(
            chat_id=user_id, text=td.AUTHORIZATION, reply_markup=await ik.user_auth()
        )


async def user_authorization(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    hi = await bot.send_message(chat_id=message.chat.id, text="Приветствую , я чат-бот NSA\n\nЗдесь вы можете задать вопрос куратору✏️\n\nПожалуйста, задавайте вопрос подробно и конкретно, чтобы специалист смог ответить на него точно.\n\nПосле того, как вы напишете вопрос, на него ответит первый освободившийся куратор. Просим вас ожидать�\\n\nТак же вы можете посмотреть историю вопросов и диалогов с куратором\n\nЧто бы задать вопрос, необходимо авторизоваться по номер телефону в формате 89000000000")
    mes = await bot.send_message(
        chat_id=message.chat.id,
        text=td.AUTHORIZATION,
        reply_markup=await ik.user_auth(),
    )
    if message.chat.id in mes_to_del:
        mes_to_del[message.chat.id].append(mes.message_id)
        mes_to_del[message.chat.id].append(hi.message_id)
    else:
        mes_to_del[message.chat.id] = [mes.message_id]


async def get_user_phone_number(call: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=td.GET_USER_PHONE,
    )
    await UserAuth.waiting_for_valid_phone.set()


async def check_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    phone_number = message.text
    mes_to_del[message.chat.id].append(message.message_id)
    if await is_phone_number_valid(phone_number):
        await state.finish()
        r = requests.get(f"https://api.nutritionscience.pro/api/v1/users/tgbot?phone={phone_number}")
            # params={"phone": "89867178660"},
        # )  #
        try:
            user: TelegramUser = await user_db.select_user(user_id)
            if user:
                try:
                    await user_db.update_user_phone(user_id=user_id, phone=phone_number)
                except:
                    await bot.delete_message(message.chat.id, message.message_id)
                    mes = await bot.send_message(
                        message.chat.id, "Пользователь с таким номером уже аторизован"
                    )
                    mes_to_del[message.chat.id].append(mes.message_id)
                    return
                await bot.delete_message(chat_id=user_id, message_id=message.message_id)
                if user.user_role == "ученик":
                    await del_mes_history(message.chat.id)
                    await bot.send_message(
                        chat_id=user_id,
                        text=td.SUCCESS_LOGIN_USR.format(user.name),
                        reply_markup=await ik.user_questions(),
                    )
                if user.user_role == "куратор":
                    await bot.send_message(
                        chat_id=user_id,
                        text=td.SUCCESS_LOGIN.format(
                            user.name,
                            f"{' ожидания вопроса' if user.state == 1 else 'деактивирован'}",
                        ),
                        reply_markup=await ik.main_kurator_menu(),
                    )
                if user.user_role == "наставник":
                    await bot.send_message(
                        chat_id=user_id,
                        text=td.SUCCESS_LOGIN.format(
                            user.name,
                            f"{'активный' if user.state == 1 else 'не активный'}",
                        ),
                        reply_markup=await ik.main_nastavnik_menu(),
                    )
                return
        except Exception as e:
            print(e)
        if phone_number not in list(await user_db.get_phones()):
            await user_db.add_user(
                user_id=user_id,
                name=message.from_user.first_name,
                role="ученик",
                phone_number=phone_number,
            )
            user = await user_db.select_user(user_id=user_id)
            result = dict(r.json())
            await _role_segregated_menu(message, result, user)
        else:
            await bot.delete_message(message.chat.id, message.message_id)
            mes = await bot.send_message(
                message.chat.id, "Пользователь с таким номером уже аторизован"
            )
            mes_to_del[message.chat.id].append(mes.message_id)

    else:
        mes = await bot.send_message(chat_id=user_id, text=td.INVALID_PHONE)
        mes_to_del[message.chat.id].append(mes.message_id)


async def _role_segregated_menu(message: types.Message, result, user: TelegramUser):
    user_id = message.from_user.id
    if result["user"] and not result["is_active"]:
        mes = await bot.send_message(
            chat_id=user_id, text=td.UNAVALIABLE_AUTH, reply_markup=await ik.user_auth()
        )
        mes_to_del[message.chat.id].append(mes.message_id)
    if result["user"] and result["is_active"]:
        if user.user_role == "ученик":
            mes = await bot.send_message(
                chat_id=user_id,
                text=td.SUCCESS_LOGIN_USR.format(user.name),
                reply_markup=await ik.user_questions(),
            )
            await del_mes_history(message.chat.id)
            mes_to_del[message.chat.id].append(mes.message_id)
        if user.user_role == "куратор":
            await bot.send_message(
                chat_id=user_id,
                text=td.SUCCESS_LOGIN.format(
                    user.name,
                    f"{' ожидания вопроса' if user.state == 1 else ' деактивирован'}",
                ),
                reply_markup=await ik.main_kurator_menu(),
            )
        if user.user_role == "наставник":
            await bot.send_message(
                chat_id=user_id,
                text=td.SUCCESS_LOGIN.format(
                    user.name, f"{'активный' if user.state == 1 else 'не активный'}"
                ),
                reply_markup=await ik.main_nastavnik_menu(),
            )
    if not result["user"] and not result["is_active"]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=td.UNAVALIABLE_AUTH_2,
            reply_markup=ik.user_auth(),
        )
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def set_user_state(call: types.CallbackQuery):
    user_id = call.from_user.id
    new_state = 1
    user: TelegramUser = await user_db.select_user(user_id)
    if user.state == 1:
        new_state = 0
    await user_db.update_user_state(user_id=user_id, state=new_state)
    await bot.edit_message_text(
        text=td.SUCCESS_LOGIN.format(
            user.name,
            f"{' <b>активный</b>' if new_state == 1 else ' <b>не активный</b>'}",
        ),
        message_id=call.message.message_id,
        chat_id=user_id,
        reply_markup=await ik.main_kurator_menu(),
    )
