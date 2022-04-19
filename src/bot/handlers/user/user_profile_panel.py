from aiogram import types

from bot.config.loader import bot
from bot.services.db import question as question_db
from bot.services.db import user as user_db
from bot.keyboards import inline as ik
from bot.data import text_data as td
from usersupport.models import UserQuestion, TelegramUser


async def get_my_questions(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = await user_db.select_user(user_id=user_id)
    await bot.edit_message_text(
        chat_id=user_id,
        text="Выберите ваш вопрос",
        message_id=call.message.message_id,
        reply_markup=await ik.get_q_list(user),
    )


async def user_pp(call: types.CallbackQuery):
    user_id = call.from_user.id
    user: TelegramUser = await user_db.select_user(user_id=user_id)
    await bot.edit_message_text(
        chat_id=user_id,
        text=td.SUCCESS_LOGIN_USR.format(user.name),
        message_id=call.message.message_id,
        reply_markup=await ik.user_questions(),
    )


async def show_q_info(call: types.CallbackQuery):
    quid = call.data.replace("quid_", "")
    user_id = call.from_user.id
    user = await user_db.select_user(user_id=user_id)
    q: UserQuestion = await question_db.select_question_by_id(user=user, pk=quid)
    await bot.edit_message_text(
        text=f"История:\n{q.history}\n Оценка:{'🌟' * int(q.rate)}\nОтзыв: {q.feedback}\n",
        chat_id=user_id,
        message_id=call.message.message_id,
        reply_markup=await ik.back_to_q_list(),
    )

