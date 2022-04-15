from aiogram import types
from aiogram.dispatcher import FSMContext

from config import config
from config.loader import bot, user_data, cur
from data import text_data as td
from keyboards import inline as ik

all = [
    "get_answer",
    "new_question",
]

from states import UserQuestion


async def get_answer(message: types.Message):
    user_id = int(message.reply_to_message.text.split("\n")[0])
    if user_id in user_data or user_id in user_data.keys():
        user_question = str(message.reply_to_message.text.split("\n\n")[1])
        mentors_answer = str(message.text)
        await bot.send_message(
            chat_id=int(user_id),
            text=td.MENTORS_ANSWER.format(user_question, mentors_answer)
        )


async def new_question(message: types.Message):
    if message.text == "завершить":
        print("sadasd")
    else:
        kur_mess_id = cur.execute('SELECT kurmes FROM data WHERE id == ?', (message.from_user.id,)).fetchone()[0]
        nast_mess_id = cur.execute('SELECT nastmes FROM data WHERE id == ?', (message.from_user.id,)).fetchone()[0]
        print(kur_mess_id)
        print(nast_mess_id)
        # print(user_data["kur_mes"])
        # us_id = message.chat.id
        # number = int(cur.execute('SELECT number FROM data WHERE id == ?', (us_id,)).fetchone()[0])
        # kur = await bot.send_message(
        #     chat_id=config.CHANNEL_KURATOR,
        #     text=td.USER_QUSTION.format(message.from_user.id, number, message.text),
        #     reply_to_message_id=user_data[us_id]["kur_mes"]
        # )
        # nast = await bot.send_message(
        #     chat_id=config.CHANNEL_NASTAVNIK,
        #     text=td.USER_QUSTION.format(us_id, number, message.text)
        # )