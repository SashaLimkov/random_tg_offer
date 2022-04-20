from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot, user_mes
from bot.data import text_data as td
from bot.keyboards import inline as ik
from bot.services.db import question as question_db
from bot.services.db import user as user_db

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
        message_id=call.message.message_id,
    )
    await UserQuestion.waiting_for_user_question.set()


async def wrong_q(call: types.CallbackQuery, state: FSMContext):
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
    await UserQuestion.waiting_for_user_question.set()


async def is_right_question(message: types.Message, state: FSMContext):
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
        question = message.text + f"|."
        # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(
            text=td.IS_IT_YOUR_QUESTION.format(question.split("|")[0]),
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


async def send_user_questions(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_question, file_id = data.get("user_question").split('|')
    await state.finish()
    user_id = call.from_user.id
    user: TelegramUser = await user_db.select_user(user_id=user_id)
    kurators, mentors = await user_db.select_all_kurators_and_mentors()
    all_kurators_list = [k.chat_id for k in kurators]
    k_list = {k.chanel_id: k.chat_id for k in kurators if k.state == 1}
    m_list = {m.chanel_id: m.chat_id for m in mentors if m.state == 1}
    text = "{}\nВопрос от пользователя {}: {}\n{}"
    history = f"Q: {user_question}\n"
    try:
        q: ModelUserQuestion = await question_db.select_question(user=user)
        user_question = f"{q.history}{history}"
        history = user_question
    except Exception:
        await question_db.add_question(user=user, question=user_question)
    q: ModelUserQuestion = await question_db.select_question(user=user)
    await question_db.add_history(user=user, pk=q.pk, history=history)
    await UserQuestion.waiting_for_new_question.set()
    if user.user_role == "ученик":
        try:
            mes: types.Message = await bot.edit_message_text(
                chat_id=user_id,
                text=td.QUESTION_SENDED,
                message_id=call.message.message_id,
                reply_markup=await ik.answer_done()
            )
        except Exception:
            await bot.delete_message(
                chat_id=user_id,
                message_id=call.message.message_id
            )
            mes: types.Message = await bot.send_message(
                chat_id=user_id,
                text=td.QUESTION_SENDED,
                reply_markup=await ik.answer_done()
            )
        user_mes[user_id] = mes.message_id
        sent_q_id_dict = {}
        for kur in k_list:
            m = await bot.send_message(chat_id=k_list[kur], text=".")
            if file_id.startswith("."):
                mes = await bot.send_message(
                    chat_id=kur,
                    text=text.format(user.user_id, user.name, user.phone, user_question),
                )
            elif file_id.startswith("photo"):
                k_file_id = file_id.replace("photo", "")
                await bot.send_photo(
                    chat_id=kur,
                    photo=k_file_id,
                    caption=text.format(user.user_id, user.name, user.phone, user_question),
                )
            elif file_id.startswith("document"):
                k_file_id = file_id.replace("document", "")
                await bot.send_document(
                    chat_id=kur,
                    document=k_file_id,
                    caption=text.format(user.user_id, user.name, user.phone, user_question),
                )
            sent_q_id_dict[k_list[kur]] = m.message_id + 1
            await bot.delete_message(chat_id=k_list[kur], message_id=m.message_id)
        for m in m_list:
            me = await bot.send_message(chat_id=m_list[m], text=".")
            if file_id.startswith("."):
                mes = await bot.send_message(
                    chat_id=m,
                    text=text.format(user.user_id, user.name, user.phone, user_question),
                )
            elif file_id.startswith("photo"):
                m_file_id = file_id.replace("photo", "")
                await bot.send_photo(
                    chat_id=m,
                    photo=m_file_id,
                    caption=text.format(user.user_id, user.name, user.phone, user_question),
                )
            elif file_id.startswith("document"):
                m_file_id = file_id.replace("document", "")
                await bot.send_document(
                    chat_id=m,
                    document=m_file_id,
                    caption=text.format(user.user_id, user.name, user.phone, user_question),
                )
            sent_q_id_dict[m_list[m]] = me.message_id + 1
            await bot.delete_message(chat_id=m_list[m], message_id=me.message_id)
        mes_id = str(sent_q_id_dict)
        await question_db.add_mes_id(user=user, mes_id=mes_id)

# async def continue_question(message: types.Message):
#     user_id = message.from_user.id
#     user: TelegramUser = await user_db.select_user(user_id=user_id)
#     q: ModelUserQuestion = await question_db.select_question(user=user)
#     user_question = message.text
#     clear_q = message.text
#     kurators, mentors = await user_db.select_all_kurators_and_mentors()
#     sent_q_id_dict = eval(q.mes_id)
#     all_kurators_list = [k.chat_id for k in kurators]
#     k_list = [k.chat_id for k in kurators if k.state == 1]
#     m_list = [m.chat_id for m in mentors if m.state == 1]
#     text = "{}: {}"
#     history = f"Q: {user_question}\n"
#     try:
#         q: ModelUserQuestion = await question_db.select_question(user=user)
#         user_question = f"{q.history}{history}"
#         history = user_question
#     except Exception:
#         await question_db.add_question(user=user, question=user_question)
#     await question_db.add_history(user=user, history=history)
#     if user.user_role == "ученик":
#         await bot.send_message(
#             chat_id=user_id,
#             text=f"Q - ваш вопрос.\nA - ответ куратора:\n{history}",
#         )
#         for kur in k_list:
#             if kur in sent_q_id_dict:
#                 await bot.send_message(
#                     chat_id=kur,
#                     text=text.format(user.name, clear_q),
#                     reply_to_message_id=sent_q_id_dict[kur]
#                 )
#         for m in m_list:
#             if m in sent_q_id_dict:
#                 await bot.send_message(
#                     chat_id=m,
#                     text=text.format(
#                         user.name,
#                         clear_q
#                     ),
#                     reply_to_message_id=sent_q_id_dict[m]
#                 )
#         mes_id = str(sent_q_id_dict)
#         await question_db.add_mes_id(user=user, mes_id=mes_id)
