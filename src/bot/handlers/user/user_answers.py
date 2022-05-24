from datetime import date
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config import config
from bot.config.loader import bot, user_data, user_mes, mes_to_del
from bot.data import text_data as td
from bot.keyboards import reply as rk
from bot.keyboards import inline as ik
from usersupport.models import TelegramUser, UserQuestion
from bot.services.db import user as user_db
from bot.services.db import question as question_db
from bot.states import UserQuestion as StateUserQuestion

all = [
    "get_answer",
    "new_question",
]


async def get_answer(message: types.Message):
    if message.reply_to_message.caption:
        user_id = int(message.reply_to_message.caption.split("\n")[0])
    else:
        user_id = int(message.reply_to_message.text.split("\n")[0])
    user: TelegramUser = await user_db.select_user(
        user_id=user_id
    )  # юзер задавший вопрос
    helper_id = message.from_user.id
    helper: TelegramUser = await user_db.select_user(
        user_id=helper_id
    )  # куратор ответивший
    question: UserQuestion = await question_db.select_question(user=user)  # вопрос
    now_helper = question.helper_id
    if helper and helper.state == 1 and helper.user_role == "куратор":
        if not question:
            return
        if helper_id != now_helper and now_helper:
            return
        # await user_db.update_user_state(
        #     user_id=helper_id, state=0
        # )  # поставили состояние у куратора "отвечает на вопрос"

        await question_db.add_helper(
            user=user, pk=question.pk, helper_id=helper_id
        )  # Добавили вопросу id отвечающего на него
        kurators, mentors = await user_db.select_all_kurators_and_mentors()
        k_list = {k.user_id: k.chat_id for k in kurators}
        m_list = [m.chat_id for m in mentors]
        m = eval(question.mes_id)
        mes_id = {message.chat.id: message.reply_to_message.message_id}
        # print(m)
        for kur in k_list:
            # print(kur)
            try:
                if kur == helper_id:
                    continue
                await bot.send_message(
                    chat_id=k_list[kur],
                    text=f"Куратор {helper.name}: {helper.phone} взялся за вопрос",
                    reply_to_message_id=m[k_list[kur]],
                )
            except:
                pass
        for m_chat_id in m_list:
            if m_chat_id in m:
                mes_id.update({m_chat_id: m[m_chat_id]})
        await question_db.add_mes_id(
            user=user, pk=question.pk, mes_id=str(mes_id)
        )  # запомнили id чатов и сообщений с вопросом пользователя у куратора, являющегося хэлпером
        # (удалили id с других чатов) и ментора
        await bot.send_message(
            chat_id=m_list[0],
            text=f"Куратор {helper.name}: {helper.phone}\n",
            reply_to_message_id=mes_id[m_list[0]],
        )  # Отправили в чат наставника инфу о том, кто взялся за вопрос

        answer = message.text
        # time = datetime.datetime.now()
        dt = datetime.combine(date.today(), datetime.now().time())
        print(dt.isoformat(timespec='minutes').replace('T', ' '))
        history = f"{question.history}A: {answer}\n"
        history2 = f"{question.history2}A: {answer}{str(dt.isoformat(timespec='minutes').replace('T', ' '))}\n"
        await question_db.add_history(user=user, pk=question.pk, history=history)
        await question_db.add_history2(user=user, pk=question.pk, history2=history2)
        try:
            await bot.delete_message(
                chat_id=user_id,
                message_id=user_mes[user_id]
            )
            # print(user_mes)
            del user_mes[user_id]
        except Exception as e:
            # print(e)
            pass
        mes = await bot.send_message(
            chat_id=user.user_id,
            text=f"{answer}",  # тут можно написать ОТВЕТ ОТ КУРАТОРА перед ответом для юзера
            reply_markup=await ik.is_get_answer(),
        )
        try:
            await bot.edit_message_reply_markup(
                chat_id=user.user_id, message_id=user_data[user.user_id], reply_markup=None
            )
        except Exception as e:
            # print(e)
            pass
        user_data[user.user_id] = mes.message_id
        await bot.send_message(
            chat_id=m_list[0],
            text=f"{helper.name}: {answer}",
            reply_to_message_id=mes_id[m_list[0]],
        )  # отправили наставнику ответ куратора
        return
    answer = message.text
    dt = datetime.combine(date.today(), datetime.now().time())
    print(dt.isoformat(timespec='minutes').replace('T', ' '))

    history = f"{question.history}A: {answer}\n"
    history2 = f"{question.history2}A: {answer}{str(dt.isoformat(timespec='minutes').replace('T', ' '))}\n"

    kurators, mentors = await user_db.select_all_kurators_and_mentors()
    k_list = {k.user_id: k.chat_id for k in kurators}
    k_all = [k.chat_id for k in kurators]
    m_list = [m.chat_id for m in mentors]
    mes_id = eval(question.mes_id)

    if helper.user_role == "куратор":
        if helper_id != now_helper and now_helper:
            return
        await bot.send_message(
            chat_id=m_list[0],
            text=f"{helper.name}: {answer}",
            reply_to_message_id=mes_id[m_list[0]],
        )  # отправили наставнику ответ куратора
    else:
        try:
            await bot.send_message(
                chat_id=k_list[question.helper_id],
                text=f"Ответ от наставника {helper.name}: {helper.phone}\n{answer}",
                reply_to_message_id=mes_id[k_list[question.helper_id]],
            )  # отправили куратору ответ от наставника
        except KeyError:
            for k_id in k_all:
                try:
                    await bot.send_message(
                        chat_id=k_id,
                        text=f"Ответ от наставника {helper.name}: {helper.phone}\n{answer}",
                        reply_to_message_id=mes_id[k_id],
                    )
                except:
                    pass
    try:
        await bot.edit_message_reply_markup(
            chat_id=user.user_id, message_id=user_data[user.user_id], reply_markup=None
        )
    except Exception as e:
        # print(e)
        pass
    try:
        await bot.delete_message(
            chat_id=user_id,
            message_id=user_mes[user_id]
        )
        del user_mes[user_id]
    except Exception as e:
        # print(e)
        pass
    await question_db.add_history(
        user=user, pk=question.pk, history=history)
    await question_db.add_history2(
        user=user, pk=question.pk, history2=history2
    )  # записали историю в бд

    await bot.edit_message_reply_markup(
            chat_id=user_id, message_id=user_mes[user_id], reply_markup=None
        )
    mes = await bot.send_message(
        chat_id=user.user_id, text=f"{answer}", reply_markup=await ik.is_get_answer()
    )
    user_mes[user.user_id] = mes.message_id
    user_data[user.user_id] = mes.message_id
    print(
        user_mes,user_data,sep="\n"
    )
    # await StateUserQuestion.wait_for_new_q_or_done.set(u)


async def answer_done(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.from_user.id
    # await bot.delete_message(
    #     chat_id=user_id,
    #     message_id=call.message.message_id
    # )
    try:
        await bot.edit_message_reply_markup(
            chat_id=user_id, message_id=call.message.message_id, reply_markup=None
        )
    except Exception as e:
        print(e)

    user: TelegramUser = await user_db.select_user(user_id=user_id)
    question: UserQuestion = await question_db.select_question(user=user)
    helper_id = question.helper_id
    await user_db.update_user_state(user_id=helper_id, state=1)
    mes = await bot.send_message(
        chat_id=user_id,
        text="Поставьте оценку",
        reply_markup=await ik.set_kurators_rate(),
    )
    mes_to_del[call.message.chat.id].append(mes.message_id)

# kur_mess_id = ...  # cur.execute('SELECT kurmes FROM data WHERE id == ?', (message.from_user.id,)).fetchone()[
# # 0]
# us_id = message.chat.id
# number = ...  # int(cur.execute('SELECT number FROM data WHERE id == ?', (us_id,)).fetchone()[0])
# if message.text == "Завершить":
#     kur = await bot.send_message(
#         chat_id=-1001735851066,
#         text=td.USER_STOP.format(number),
#         reply_to_message_id=kur_mess_id
#     )
#     await bot.send_message(
#         chat_id=config.CHANNEL_NASTAVNIK,
#         text=td.USER_STOP.format(number)
#     )
#     await bot.send_message(chat_id=us_id,
#                            text="Поставьте нам оценку!",
#                            reply_markup=await ik.set_kurators_rate())
#     # await state.finish()
# else:
#     kur = await bot.send_message(
#         chat_id=-1001735851066,
#         text=td.USER_QUSTION.format(message.from_user.id, number, message.text),
#         reply_to_message_id=kur_mess_id
#     )
#     await bot.send_message(
#         chat_id=-1001741967870,
#         text=td.USER_QUSTION.format(message.from_user.id, number, message.text)
#     )
