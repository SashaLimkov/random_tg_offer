from aiogram import types
from aiogram.dispatcher import FSMContext

from src.bot.config import config
from src.bot.config.loader import bot, cur, user_data
from src.bot.data import text_data as td
from src.bot.keyboards import inline as ik

__all__ = [
    "create_user_question",
    "is_right_question",
    "send_user_questions",
    "add_question",
]

from src.bot.states import UserQuestion


async def create_user_question(call: types.CallbackQuery):
    await bot.edit_message_text(
        text=td.ASK_A_QUESTION,
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
    )
    await UserQuestion.waiting_for_user_question.set()


async def add_question(call: types.CallbackQuery):
    print("HERE!")
    # await bot.edit_message_text(
    #     text=td.ASK_A_QUESTION,
    #     chat_id=call.from_user.id,
    #     message_id=call.message.message_id
    # )
    # await UserQuestion.waiting_for_user_question.set()


async def is_right_question(message: types.Message, state: FSMContext):
    question = message.text
    await state.update_data(user_question=question)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(
        text=td.IS_IT_YOUR_QUESTION.format(question),
        chat_id=message.chat.id,
        reply_markup=await ik.is_question_right(),
    )


async def send_user_questions(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_question = data.get("user_question")
    await state.finish()
    us_id = call.from_user.id
    user_state = int(
        cur.execute("SELECT state FROM data WHERE id == ?", (us_id,)).fetchone()[0]
    )
    role = cur.execute("SELECT role FROM data WHERE id == ?", (us_id,)).fetchone()[0]
    number = int(
        cur.execute("SELECT number FROM data WHERE id == ?", (us_id,)).fetchone()[0]
    )
    if role == td.ROLE_USER and user_state == 1:
        await UserQuestion.waiting_for_answer.set()
        try:
            if user_data[us_id]:
                await bot.edit_message_text(
                    chat_id=us_id,
                    text=td.QUESTION_SENDED,
                    message_id=call.message.message_id,
                )
                kur = await user_data[us_id]["kur_msg"].reply(
                    text=td.USER_QUSTION.format(us_id, number, user_question)
                )
                nast = await user_data[us_id]["nast_msg"].reply(
                    text=td.USER_QUSTION.format(us_id, number, user_question)
                )
                user_data[us_id] = {"kur_mes": kur, "nast_mes": nast}
        except KeyError:
            await bot.edit_message_text(
                chat_id=us_id,
                text=td.QUESTION_SENDED,
                message_id=call.message.message_id,
            )
            kur = await bot.send_message(
                chat_id=config.CHANNEL_KURATOR,
                text=td.USER_QUSTION.format(us_id, number, user_question),
            )
            nast = await bot.send_message(
                chat_id=config.CHANNEL_NASTAVNIK,
                text=td.USER_QUSTION.format(us_id, number, user_question),
            )
            user_data[us_id] = {"kur_mes": kur, "nast_mes": nast}
