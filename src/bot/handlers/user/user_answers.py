from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config import config
from bot.config.loader import bot, user_data, user_mes
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
        try:
            await bot.delete_message(
                chat_id=user_id,
                message_id=user_mes[user_id]
            )
            del user_mes[user_id]
        except Exception as e:
            print("222222222222222222222222222222222222222222222")
            print(e)
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
    try:
        await bot.delete_message(
            chat_id=user_id,
            message_id=user_mes[user_id]
        )
        del user_mes[user_id]
    except Exception as e:
        print("11111111111111111111111111111111111111111111111111")
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
    user_id = call.from_user.id
    mes_id = call.message.message_id
    try:
        await bot.edit_message_text(
            text=td.ASK_A_QUESTION,
            chat_id=user_id,
            message_id=mes_id,
        )
    except Exception:
        await bot.delete_message(
            chat_id=user_id,
            message_id=mes_id
        )
        await bot.send_message(
            text=td.ASK_A_QUESTION,
            chat_id=user_id,
        )
    await state.finish()
    await StateUserQuestion.waiting_for_new_question.set()


async def is_right_new_question(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    if message.media_group_id:
        await bot.send_message(
            chat_id=user_id,
            text='Вы можете отправить только текст с фотографией , либо по отдельности'
        )
        return
    elif message.photo:
        question = message.caption + f"|photo{message.photo[-1].file_id}" if message.caption else f"ВОПРОС С ФОТО|photo{message.photo[-1].file_id}"
        await bot.send_photo(
            chat_id=user_id,
            photo=message.photo[-1].file_id,
            caption=td.IS_IT_YOUR_QUESTION.format(question.split("|")[0]),
            reply_markup=await ik.is_question_right()
        )
    elif message.document:
        question = message.caption + f"|document{message.document.file_id}" if message.caption else f"ВОПРОС С ФОТО|document{message.document.file_id}"
        await bot.send_document(
            chat_id=user_id,
            document=message.document.file_id,
            caption=td.IS_IT_YOUR_QUESTION.format(question.split("|")[0]),
            reply_markup=await ik.is_question_right()
        )
    elif message.text:
        question = message.text
        await bot.send_message(
            text=td.IS_IT_YOUR_QUESTION.format(question),
            chat_id=message.chat.id,
            reply_markup=await ik.is_question_right(),
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text='Вы можете отправить только текст с фотографией , либо по отдельности'
        )
        return
    await state.update_data(user_question=question)


async def send_new_question(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_question, file_id = data.get("user_question").split('|')
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
        if file_id.startswith("."):
            await bot.send_message(
                chat_id=k_list[helper_id],
                text=f"{user.name}: {user_question}",
                reply_to_message_id=mes_id[k_list[helper_id]],
            )
            await bot.send_message(
                chat_id=m_list[0],
                text=f"{user.name}: {user_question}",
                reply_to_message_id=mes_id[m_list[0]],
            )  # вопрос наставнику
        elif file_id.startswith("photo"):
            k_file_id = file_id.replace("photo", "")
            await bot.send_photo(
                chat_id=k_list[helper_id],
                photo=k_file_id,
                caption=f"{user.name}: {user_question}",
                reply_to_message_id=mes_id[k_list[helper_id]],
            )
            await bot.send_photo(
                chat_id=m_list[0],
                photo=k_file_id,
                text=f"{user.name}: {user_question}",
                reply_to_message_id=mes_id[m_list[0]],
            )  # вопрос наставнику
        elif file_id.startswith("document"):
            k_file_id = file_id.replace("document", "")
            await bot.send_document(
                chat_id=k_list[helper_id],
                document=k_file_id,
                caption=f"{user.name}: {user_question}",
                reply_to_message_id=mes_id[k_list[helper_id]],
            )
            await bot.send_document(
                chat_id=m_list[0],
                document=k_file_id,
                text=f"{user.name}: {user_question}",
                reply_to_message_id=mes_id[m_list[0]],
            )  # вопрос наставнику
        # await bot.send_message(
        #     chat_id=k_list[helper_id],
        #     text=f"{user.name}: {user_question}",
        #     reply_to_message_id=mes_id[k_list[helper_id]],
        # )  # вопрос к куратору
    except:
        for kur in k_list:
            if file_id.startswith("."):
                await bot.send_message(
                    chat_id=k_list[kur],
                    text=f"{user.name}: {user_question}",
                    reply_to_message_id=mes_id[k_list[kur]],
                )
                await bot.send_message(
                    chat_id=m_list[0],
                    text=f"{user.name}: {user_question}",
                    reply_to_message_id=mes_id[m_list[0]],
                )  # вопрос наставнику
            elif file_id.startswith("photo"):
                k_file_id = file_id.replace("photo", "")
                await bot.send_photo(
                    chat_id=k_list[kur],
                    photo=k_file_id,
                    caption=f"{user.name}: {user_question}",
                    reply_to_message_id=mes_id[k_list[kur]],
                )
                await bot.send_photo(
                    chat_id=m_list[0],
                    photo=k_file_id,
                    text=f"{user.name}: {user_question}",
                    reply_to_message_id=mes_id[m_list[0]],
                )  # вопрос наставник
            elif file_id.startswith("document"):
                k_file_id = file_id.replace("document", "")
                await bot.send_document(
                    chat_id=k_list[kur],
                    document=k_file_id,
                    caption=f"{user.name}: {user_question}",
                    reply_to_message_id=mes_id[k_list[kur]],
                )
                await bot.send_document(
                    chat_id=m_list[0],
                    document=k_file_id,
                    text=f"{user.name}: {user_question}",
                    reply_to_message_id=mes_id[m_list[0]],
                )

            # await bot.send_message(
            #     chat_id=k_list[kur],
            #     text=f"{user.name}: {user_question}",
            #     reply_to_message_id=mes_id[k_list[kur]],
            # )  # вопрос к кураторам
    await bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
    try:
        await bot.delete_message(
            chat_id=user_id,
            message_id=user_mes[user_id]
        )
        del user_mes[user_id]
    except:
        pass
    mes = await bot.send_message(chat_id=user_id, text=td.QUESTION_SENDED, reply_markup=await ik.answer_done())
    user_mes[user_id] = mes.message_id


async def answer_done(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.from_user.id
    await bot.delete_message(
        chat_id=user_id,
        message_id=call.message.message_id
    )
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
