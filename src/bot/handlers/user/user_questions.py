from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config import config
from bot.config.loader import bot, user_data
from bot.data import text_data as td
from bot.keyboards import inline as ik
from bot.services.db import user as user_db

__all__ = [
    "create_user_question",
    "is_right_question",
    "send_user_questions",
]

from bot.states import UserQuestion
from usersupport.models import TelegramUser


async def create_user_question(call: types.CallbackQuery):
    await bot.edit_message_text(
        text=td.ASK_A_QUESTION,
        chat_id=call.from_user.id,
        message_id=call.message.message_id
    )
    await UserQuestion.waiting_for_user_question.set()


# async def add_question(call: types.CallbackQuery):
#     print("HERE!")
#     # await bot.edit_message_text(
#     #     text=td.ASK_A_QUESTION,
#     #     chat_id=call.from_user.id,
#     #     message_id=call.message.message_id
#     # )
#     # await UserQuestion.waiting_for_user_question.set()


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
    role = user.user_role
    number = user.phone
    if role == "ученик":
        await bot.edit_message_text(
            chat_id=user_id,
            text=td.QUESTION_SENDED,
            message_id=call.message.message_id
        )
        kur = await bot.send_message(
            chat_id=config.CHANNEL_KURATOR,
            text=td.USER_QUSTION.format(user_id, number, user_question)
        )
        user_data[user_id] = {"kur_mes": kur}
        # cur.execute('UPDATE data SET kurmes == ? WHERE id == ?',
        #             (kur.message_id, call.from_user.id))
        # base.commit()
