from aiogram import types

from bot.config.loader import bot
from bot.services.db import question as question_db
from bot.services.db import user as user_db
from bot.keyboards import inline as ik
from usersupport.models import UserQuestion


async def get_my_questions(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.edit_message_text(
        chat_id=user_id,
        text="Выберите ваш вопрос",
        message_id=call.message.message_id,
        reply_markup=await ik.get_q_list()
    )


async def show_q_info(call: types.CallbackQuery):
    quid = call.data.replace("quid_", "")
    user_id = call.from_user.id
    user = await user_db.select_user(user_id=user_id)
    q: UserQuestion = await question_db.select_question_by_id(user=user, pk=quid)
    await bot.edit_message_text(
        text=f"История:\n{q.history}\n Оценка:{'🌟' * int(q.rate)}\nОтзыв: {q.feedback}\nНапишите /lk, чтобы продолжить пользоваться",
        chat_id=user_id,
        message_id=call.message.message_id
    )
