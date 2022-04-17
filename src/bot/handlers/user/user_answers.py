
from aiogram import types

from config import config
from config.loader import bot, user_data, kurators_state
from data import text_data as td
from keyboards import reply as rk
from keyboards import inline as ik

all = [
    "get_answer",
    "new_question",
]


async def get_answer(message: types.Message):
    user_id = int(message.reply_to_message.text.split("\n")[0])
    # cur.execute('UPDATE data SET kurmes == ? WHERE id == ?',
    #             (message.reply_to_message.message_id, message.from_user.id))
    # base.commit()
    try:
        if kurators_state[message.from_user.id]:
            pass
    except:
        if message.chat.id == -1001735851066:
            kurators_state[message.from_user.id] = 1
            number = message.reply_to_message.text.split("\n")[1]
            nast = await bot.send_message(
                chat_id=-1001506209957,
                text=f'Куратор {message.from_user.first_name}, консультирует пользователя с номером '
                     f'{number}')
    finally:
        if user_id in user_data or user_id in user_data.keys():
            if message.chat.id == -1001741967870:
                user_question = str(message.reply_to_message.text.split("\n")[1])
                mentors_answer = str(message.text)
                await bot.send_message(
                    chat_id=-1001735851066,
                    text=f'Наставник {message.from_user.first_name} ответил пользователю за вас.\n' + td.MENTORS_ANSWER.format(
                        user_question, mentors_answer))
                await bot.send_message(
                    chat_id=int(user_id),
                    text=td.MENTORS_ANSWER.format(user_question, mentors_answer),
                    reply_markup=rk.stop_keyboard
                )
            else:
                user_question = str(message.reply_to_message.text.split("\n\n")[1])
                mentors_answer = str(message.text)
                await bot.send_message(
                    chat_id=int(user_id),
                    text=td.MENTORS_ANSWER.format(user_question, mentors_answer),
                    reply_markup=rk.stop_keyboard
                )
            await bot.send_message(
                chat_id=config.CHANNEL_NASTAVNIK,
                text=f"{user_id}\nПользовательский {user_question}\nОтвет от куратора {message.from_user.first_name}: {mentors_answer}"
            )
            # await NewQuestions.new_q.set()


async def new_question(message: types.Message):
    print("ЗДЕСЬ")
    kur_mess_id = ... #cur.execute('SELECT kurmes FROM data WHERE id == ?', (message.from_user.id,)).fetchone()[
        # 0]
    us_id = message.chat.id
    number = ... #int(cur.execute('SELECT number FROM data WHERE id == ?', (us_id,)).fetchone()[0])
    if message.text == "Завершить":
        kur = await bot.send_message(
            chat_id=-1001735851066,
            text=td.USER_STOP.format(number),
            reply_to_message_id=kur_mess_id
        )
        await bot.send_message(
            chat_id=config.CHANNEL_NASTAVNIK,
            text=td.USER_STOP.format(number)
        )
        await bot.send_message(chat_id=us_id,
                               text="Поставьте нам оценку!",
                               reply_markup=await ik.set_kurators_rate())
        # await state.finish()
    else:
        kur = await bot.send_message(
            chat_id=-1001735851066,
            text=td.USER_QUSTION.format(message.from_user.id, number, message.text),
            reply_to_message_id=kur_mess_id
        )
        await bot.send_message(
            chat_id=-1001741967870,
            text=td.USER_QUSTION.format(message.from_user.id, number, message.text)
        )

