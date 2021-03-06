from aiogram import types

from src.bot.config.loader import bot
from src.bot.data import text_data as td
from src.bot.keyboards import inline as ik


async def get_answer(message: types.Message):
    user_id = int(message.reply_to_message.text.split("\n")[0])
    user: TelegramUser = await user_db.select_user(
        user_id=user_id
    )  # юзер задавший вопрос
    helper_id = message.from_user.id
    helper: TelegramUser = await user_db.select_user(
        user_id=helper_id
    )  # куратор ответивший
    question: UserQuestion = await question_db.select_question(user=user)  # вопрос
    if helper.state == 1 and helper.user_role == "куратор":
        await user_db.update_user_state(
            user_id=helper_id, state=0
        )  # поставили состояние у куратора "отвечает на вопрос"

        await question_db.add_helper(
            user=user, helper_id=helper_id
        )  # Добавили вопросу id отвечающего на него
        kurators, mentors = await user_db.select_all_kurators_and_mentors()
        m_list = [m.chat_id for m in mentors]
        m = eval(question.mes_id)
        mes_id = {message.chat.id: message.reply_to_message.message_id}
        for m_chat_id in m_list:
            if m_chat_id in m:
                mes_id.update({m_chat_id: m[m_chat_id]})
        await question_db.add_mes_id(
            user=user, mes_id=str(mes_id)
        )  # запомнили id чатов и сообщений с вопросом пользователя у куратора, являющегося хэлпером
        # (удалили id с других чатов) и ментора
        await bot.send_message(
            chat_id=m_list[0],
            text=f"Куратор {helper.name}: {helper.phone}\n",
            reply_to_message_id=mes_id[m_list[0]],
        )  # Отправили в чат наставника инфу о том, кто взялся за вопрос
        answer = message.text
        history = f"{question.history}A: {answer}\n"
        await question_db.add_history(user=user, pk=question.pk, history=history)
        mes = await bot.send_message(
            chat_id=user.user_id,
            text=f"{answer}",  # тут можно написать ОТВЕТ ОТ КУРАТОРА перед ответом для юзера
            reply_markup=await ik.is_get_answer(),
        )
        user_data[user.user_id] = mes.message_id
        await bot.send_message(
            chat_id=m_list[0],
            text=f"{helper.name}: {answer}",
            reply_to_message_id=mes_id[m_list[0]],
        )  # отправили наставнику ответ куратора
        return
    answer = message.text
    history = f"{question.history}A: {answer}\n"

    kurators, mentors = await user_db.select_all_kurators_and_mentors()
    k_list = {k.user_id: k.chat_id for k in kurators}
    k_all = [k.chat_id for k in kurators]
    m_list = [m.chat_id for m in mentors]
    mes_id = eval(question.mes_id)
    await question_db.add_history(
        user=user, pk=question.pk, history=history
    )  # записали историю в бд
    if helper.user_role == "куратор":
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
                await bot.send_message(
                    chat_id=k_id,
                    text=f"Ответ от наставника {helper.name}: {helper.phone}\n{answer}",
                    reply_to_message_id=mes_id[k_id],
                )
    try:
        await bot.edit_message_reply_markup(
            chat_id=user.user_id, message_id=user_data[user.user_id], reply_markup=None
        )
    except Exception as e:
        print(e)
    mes = await bot.send_message(
        chat_id=user.user_id, text=f"{answer}", reply_markup=await ik.is_get_answer()
    )
    user_data[user.user_id] = mes.message_id
    # await StateUserQuestion.wait_for_new_q_or_done.set(u)


async def new_question(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.from_user.id
    try:
        await bot.edit_message_reply_markup(
            chat_id=user_id, message_id=user_data[user_id], reply_markup=None
        )
    except Exception as e:
        print(e)
    await bot.send_message(
        chat_id=user_id,
        text=td.ASK_A_QUESTION,
    )
    await StateUserQuestion.waiting_for_new_question.set()


async def wrong_question(call: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        text=td.ASK_A_QUESTION,
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
    )
    await state.finish()
    await StateUserQuestion.waiting_for_new_question.set()


async def is_right_new_question(message: types.Message, state: FSMContext):
    question = message.text
    await state.update_data(user_question=question)
    await bot.send_message(
        text=td.IS_IT_YOUR_QUESTION.format(question),
        chat_id=message.chat.id,
        reply_markup=await ik.is_new_question_right(),
    )


async def send_new_question(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_question = data.get("user_question")
    await state.finish()
    user_id = call.from_user.id
    user: TelegramUser = await user_db.select_user(user_id=user_id)
    question: UserQuestion = await question_db.select_question(user=user)
    helper_id = question.helper_id
    mes_id = eval(question.mes_id)
    q = f"Q: {user_question}\n"
    history = f"{question.history}{q}\n"
    await question_db.add_history(user=user, pk=question.pk, history=history)
    kurators, mentors = await user_db.select_all_kurators_and_mentors()
    k_list = {k.user_id: k.chat_id for k in kurators}
    m_list = [m.chat_id for m in mentors]
    try:
        await bot.send_message(
            chat_id=k_list[helper_id],
            text=f"{user.name}: {user_question}",
            reply_to_message_id=mes_id[k_list[helper_id]],
        )  # вопрос к куратору
    except:
        for kur in k_list:
            await bot.send_message(
                chat_id=k_list[kur],
                text=f"{user.name}: {user_question}",
                reply_to_message_id=mes_id[k_list[kur]],
            )  # вопрос к кураторам
    await bot.send_message(
        chat_id=m_list[0],
        text=f"{user.name}: {user_question}",
        reply_to_message_id=mes_id[m_list[0]],
    )  # вопрос наставнику
    await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
    await bot.send_message(chat_id=user_id, text=td.QUESTION_SENDED)


async def answer_done(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.from_user.id
    try:
        await bot.edit_message_reply_markup(
            chat_id=user_id, message_id=user_data[user_id], reply_markup=None
        )
    except Exception as e:
        print(e)

    user: TelegramUser = await user_db.select_user(user_id=user_id)
    question: UserQuestion = await question_db.select_question(user=user)
    helper_id = question.helper_id
    await user_db.update_user_state(user_id=helper_id, state=1)
    await bot.send_message(
        chat_id=user_id,
        text="Поставьте оценку",
        reply_markup=await ik.set_kurators_rate(),
    )


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
=======
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
