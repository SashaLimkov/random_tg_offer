from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import bot.config.config
from bot.config.loader import bot, mes_to_del
from bot.handlers.user.cleaner import del_mes_history
from bot.keyboards import reply as rk
from bot.keyboards import inline as ik
from bot.data import text_data as td
from bot.states import Rate
from usersupport.models import TelegramUser, UserQuestion
from bot.services.db import user as user_db
from bot.services.db import question as question_db


async def set_rate(call: types.CallbackQuery):
    user_id = call.from_user.id
    user: TelegramUser = await user_db.select_user(user_id=user_id)
    rate = call.data.replace("r_", "")
    question: UserQuestion = await question_db.select_question(user=user)

    await question_db.update_rate(user=user, pk=question.pk, rate=rate)
    # await user_db.update_user_state(user_id=helper_id, state=1)
    print(question.rate)
    await bot.edit_message_reply_markup(
        chat_id=user_id, message_id=call.message.message_id
    )
    if int(rate) <=2:
        await Rate.waiting_for_rate.set()
        mes = await bot.send_message(
            chat_id=call.from_user.id,
            text='Нам жаль, что Вам не понравилось общение в чат-боте, подскажите, что  именно Вам не понравилось? Будем благодарны за обратную связь',
            reply_markup=rk.no_comment_keyboard,
        )
        mes_to_del[call.message.chat.id].append(mes.message_id)
    elif int(rate) == 3:
        await Rate.waiting_for_rate.set()
        mes = await bot.send_message(
            chat_id=call.from_user.id,
            text="Благодарим за вашу оценку, подскажите, что мы можем улучшить для комфортного взаимодействия с Вами?",
            reply_markup=rk.no_comment_keyboard,
        )
        mes_to_del[call.message.chat.id].append(mes.message_id)
    else:
        await question_db.update_feedback(
            user=user, pk=question.pk, feedback="Пользователь не оставил отзыв"
        )
        question: UserQuestion = await question_db.select_question(user=user)
        helper_id = question.helper_id
        mes_id = eval(question.mes_id)
        kurators, mentors = await user_db.select_all_kurators_and_mentors()
        k_list = {k.user_id: k.chat_id for k in kurators}
        m_list = [m.chat_id for m in mentors]
        text = f"Пользователь закрыл вопрос.\nОценка пользователя:{'🌟' * int(question.rate)}\nОтзыв: {question.feedback}"
        await question_db.update_state(user=user, pk=question.pk)
        try:
            await bot.send_message(
                chat_id=k_list[helper_id],
                text="Пользователь закрыл вопрос",
                reply_to_message_id=mes_id[k_list[helper_id]]
            )  # вопрос к куратору
        except:
            for kur in k_list:
                try:
                    await bot.send_message(
                        chat_id=k_list[kur],
                        text="Пользователь закрыл вопрос",
                        reply_to_message_id=mes_id[k_list[kur]]
                    )  # вопрос к куратору
                except:
                    pass
        await bot.send_message(
            chat_id=m_list[0], text=text, reply_to_message_id=mes_id[m_list[0]]
        )  # вопрос наставнику

        if int(question.rate) == 5 or int(question.rate) == 4:
            mes = await bot.send_message(
                chat_id=user_id,
                text=td.RATE45.format(user.name),
                reply_markup=ReplyKeyboardRemove(),
            )
            await bot.delete_message(user_id, mes.message_id)
            await del_mes_history(call.message.chat.id)
            await bot.send_message(
                chat_id=user_id,
                text=td.RATE45.format(user.name),
                reply_markup=await ik.user_questions(),
            )
        elif int(question.rate) == 3:
            mes = await bot.send_message(
                chat_id=user_id,
                text=td.RATE3.format(user.name),
                reply_markup=ReplyKeyboardRemove(),
            )
            await bot.delete_message(user_id, mes.message_id)
            await del_mes_history(call.message.chat.id)
            await bot.send_message(
                chat_id=user_id,
                text=td.RATE3.format(user.name),
                reply_markup=await ik.user_questions(),
            )
        elif int(question.rate) == 2 or int(question.rate) == 1:
            mes = await bot.send_message(
                chat_id=user_id,
                text=td.RATE12.format(user.name),
                reply_markup=ReplyKeyboardRemove(),
            )
            await bot.delete_message(user_id, mes.message_id)
            await del_mes_history(call.message.chat.id)
            await bot.send_message(
                chat_id=user_id,
                text=td.RATE12.format(user.name),
                reply_markup=await ik.user_questions(),
            )



async def get_rate(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    user: TelegramUser = await user_db.select_user(user_id=user_id)
    question: UserQuestion = await question_db.select_question(user=user)
    if message.text == "Не оставлять отзыв":
        await question_db.update_feedback(
            user=user, pk=question.pk, feedback="Пользователь не оставил отзыв"
        )
    else:
        await question_db.update_feedback(
            user=user, pk=question.pk, feedback=message.text
        )
    helper_id = question.helper_id
    mes_id = eval(question.mes_id)
    kurators, mentors = await user_db.select_all_kurators_and_mentors()
    k_list = {k.user_id: k.chat_id for k in kurators}
    m_list = [m.chat_id for m in mentors]
    question: UserQuestion = await question_db.select_question(user=user)
    text = f"Пользователь закрыл вопрос.\nОценка пользователя:{'🌟' * int(question.rate)}\nОтзыв: {question.feedback}"
    try:
        await bot.send_message(
            chat_id=k_list[helper_id],
            text="Пользователь закрыл вопрос",
            reply_to_message_id=mes_id[k_list[helper_id]]
        )  # вопрос к куратору
    except:
        for kur in k_list:
            await bot.send_message(
                chat_id=k_list[kur],
                text="Пользователь закрыл вопрос",
                reply_to_message_id=mes_id[k_list[kur]]
            )  # вопрос к кураторам
    await bot.send_message(
        chat_id=m_list[0], text=text, reply_to_message_id=mes_id[m_list[0]]
    )  # вопрос наставнику
    await question_db.update_state(user=user, pk=question.pk)

    if int(question.rate) == 5 or int(question.rate) == 4:
        mes = await bot.send_message(
            chat_id=user_id,
            text=td.RATE45.format(user.name),
            reply_markup=ReplyKeyboardRemove(),
        )
        await bot.delete_message(user_id, mes.message_id)
        await bot.delete_message(user_id, message.message_id)
        await del_mes_history(message.chat.id)
        await bot.send_message(
            chat_id=user_id,
            text=td.RATE45.format(user.name),
            reply_markup=await ik.user_questions(),
        )

    elif int(question.rate) == 3:
        mes = await bot.send_message(
            chat_id=user_id,
            text=td.RATE3.format(user.name),
            reply_markup=ReplyKeyboardRemove(),
        )
        await bot.delete_message(user_id, mes.message_id)
        await bot.delete_message(user_id, message.message_id)
        await del_mes_history(message.chat.id)
        await bot.send_message(
            chat_id=user_id,
            text=td.RATE3.format(user.name),
            reply_markup=await ik.user_questions(),
        )

    elif int(question.rate) == 2 or int(question.rate) == 1:
        mes = await bot.send_message(
            chat_id=user_id,
            text=td.RATE12.format(user.name),
            reply_markup=ReplyKeyboardRemove(),
        )
        await bot.delete_message(user_id, mes.message_id)
        await bot.delete_message(user_id, message.message_id)
        await del_mes_history(message.chat.id)
        await bot.send_message(
            chat_id=user_id,
            text=td.RATE12.format(user.name),
            reply_markup=await ik.user_questions(),
        )

