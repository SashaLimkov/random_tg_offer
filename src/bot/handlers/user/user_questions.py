import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config import config
from bot.config.loader import bot, user_data
from bot.data import text_data as td
from bot.keyboards import inline as ik
from bot.services.db import user as user_db
from bot.services.db import question as question_db

__all__ = [
    "create_user_question",
    "is_right_question",
    "send_user_questions",
]

from bot.states import UserQuestion
from usersupport.models import UserQuestion as ModelUserQuestion
from usersupport.models import TelegramUser


async def create_user_question(call: types.CallbackQuery):
    await bot.edit_message_text(
        text=td.ASK_A_QUESTION,
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )
    await UserQuestion.waiting_for_user_question.set()


async def wrong_q(call: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        text=td.ASK_A_QUESTION,
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )
    await state.finish()
    await UserQuestion.waiting_for_user_question.set()


async def is_right_question(message: types.Message, state: FSMContext):
    question = message.text
    await state.update_data(user_question=question)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(
        text=td.IS_IT_YOUR_QUESTION.format(question),
        chat_id=message.chat.id,
        reply_markup=await ik.is_question_right()
    )


async def send_user_questions(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_question = data.get("user_question")
    await state.finish()
    user_id = call.from_user.id
    user: TelegramUser = await user_db.select_user(user_id=user_id)
    kurators, mentors = await user_db.select_all_kurators_and_mentors()
    all_kurators_list = [k.chat_id for k in kurators]
    k_list = [k.chanel_id for k in kurators if k.state == 1]
    m_list = [m.chanel_id for m in mentors if m.state == 1]
    text = "{}\nВопрос от пользователя {}: {}\n{}"
    history = f"Q: {user_question}\n"
    try:
        q: ModelUserQuestion = await question_db.select_question(user=user)
        user_question = f"{q.history}{history}"
        history = user_question
    except Exception:
        await question_db.add_question(user=user, question=user_question)
    await question_db.add_history(user=user, history=history)
    # if not k_list: если все кураторы заняты
    #     random_kurator = random.choice(all_kurators_list)
    #
    if user.user_role == "ученик":
        await bot.edit_message_text(
            chat_id=user_id,
            text=td.QUESTION_SENDED,
            message_id=call.message.message_id
        )
        for kur in k_list:
            await bot.send_message(
                chat_id=kur,
                text=text.format(
                    user.user_id,
                    user.name,
                    user.phone,
                    user_question
                )
            )
        for m in m_list:
            await bot.send_message(
                chat_id=m,
                text=text.format(
                    user.user_id,
                    user.name,
                    user.phone,
                    user_question
                )
            )
        # user_data[user_id] = {"kur_mes": kur}
        # cur.execute('UPDATE data SET kurmes == ? WHERE id == ?',
        #             (kur.message_id, call.from_user.id))
        # base.commit()
