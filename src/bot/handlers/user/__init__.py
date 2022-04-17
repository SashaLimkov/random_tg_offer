from aiogram import Dispatcher, types
from aiogram.dispatcher import filters

from bot.handlers.user import setup_role, user_authorization, user_questions, save_chats
from bot.states import UserAuth, UserQuestion, Rate, Role
from bot.data import keyboards_data as kd


def setup(dp: Dispatcher):
    # setup user roles
    dp.register_message_handler(setup_role.setup_user_role, filters.Command("setup"))
    dp.register_message_handler(setup_role.check_key, state=Role.secret_key)
    # user auth
    dp.register_message_handler(user_authorization.get_profile_panel, filters.Command("lk"))
    dp.register_message_handler(user_authorization.user_authorization, filters.CommandStart())
    dp.register_callback_query_handler(
        user_authorization.get_user_phone_number,
        lambda call: call.data == kd.AUTHORIZATION_CD
    )
    dp.register_message_handler(
        user_authorization.check_phone,
        state=UserAuth.waiting_for_valid_phone
    )
    # kurators state
    dp.register_callback_query_handler(
        user_authorization.set_user_state,
        lambda call: call.data == kd.KUR_ACTIVITY_CD
    )
    dp.register_message_handler(save_chats.update_chanel, lambda message: message.forward_from_chat)

    # user ask a question
    dp.register_callback_query_handler(
        user_questions.create_user_question,
        lambda call: call.data == kd.ASK_A_QUESTION_CD
    )
    dp.register_callback_query_handler(
        user_questions.wrong_q,
        lambda call: call.data == kd.WRONG_QUESTION_CD,
        state=UserQuestion.waiting_for_user_question)
    dp.register_callback_query_handler(
        user_questions.send_user_questions,
        lambda call: call.data == kd.RIGHT_QUESTION_CD,
        state=UserQuestion.waiting_for_user_question
    )
    dp.register_message_handler(user_questions.is_right_question, state=UserQuestion.waiting_for_user_question)
    # dp.register_callback_query_handler(
    #     user_questions.create_user_question,
    #     state=UserQuestion.waiting_for_user_question
    # )
    # add chanel_and_chat_id

    # dp.register_message_handler(user_answers.get_answer, lambda message: message.reply_to_message)
    # dp.register_message_handler(user_authorization.get_profile_panel, filters.Command("lk"))
    # dp.register_callback_query_handler(kur_rate.set_rate, lambda call: call.data.startswith("r_"))
    # dp.register_message_handler(kur_rate.get_rate, state=Rate.waiting_for_rate)
    # dp.register_message_handler(user_answers.new_question)
