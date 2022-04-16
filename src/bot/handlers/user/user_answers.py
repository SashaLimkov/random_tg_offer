from aiogram import types

from src.bot.config.loader import bot
from src.bot.data import text_data as td
from src.bot.keyboards import inline as ik


async def get_answer(message: types.Message):
    # print(user_data[message.from_user.id])
    user_id = message.reply_to_message.text.split("\n")[0]
    user_question = message.reply_to_message.text.split("\n\n")[1]
    mentors_answer = message.text
    await bot.send_message(
        chat_id=user_id,
        text=td.MENTORS_ANSWER.format(user_question, mentors_answer),
        reply_markup=await ik.is_get_answer(),
    )


async def echo(call: types.CallbackQuery):
    print(call.data)
