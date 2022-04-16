from aiogram import Dispatcher
from aiogram.dispatcher import filters

from src.bot.data import keyboards_data as kd
from src.bot.handlers.user import user_questions, user_answers
from src.bot.handlers.user import user_authorization
from src.bot.states import UserAuth, UserQuestion


def setup(dp: Dispatcher):
    dp.register_message_handler(
        user_authorization.user_authorization, filters.CommandStart()
    )
    dp.register_message_handler(
        user_authorization.get_profile_panel, filters.Command("lk")
    )
    dp.register_callback_query_handler(
        user_questions.add_question, lambda call: call.data == kd.ANSWER_DONE_CD
    )
    dp.register_callback_query_handler(
        user_authorization.get_user_phone_number,
        lambda call: call.data == kd.AUTHORIZATION_CD,
    )
    dp.register_callback_query_handler(
        user_questions.create_user_question,
        lambda call: call.data == kd.ASK_A_QUESTION_CD,
    )
    dp.register_callback_query_handler(
        user_questions.send_user_questions,
        lambda call: call.data == kd.RIGHT_QUESTION_CD,
        state=UserQuestion.waiting_for_user_question,
    )
    dp.register_callback_query_handler(
        user_questions.create_user_question,
        state=UserQuestion.waiting_for_user_question,
    )
    dp.register_message_handler(
        user_questions.is_right_question, state=UserQuestion.waiting_for_user_question
    )
    dp.register_message_handler(
        user_authorization.check_phone, state=UserAuth.waiting_for_valid_phone
    )
    dp.register_message_handler(
        user_answers.get_answer, lambda message: message.reply_to_message
    )
    dp.register_callback_query_handler(user_answers.echo)
