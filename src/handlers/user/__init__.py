from aiogram import Dispatcher, types
from aiogram.dispatcher import filters

from data import keyboards_data as kd
from handlers.user import user_authorization, user_questions, user_answers, kur_rate
from states import UserAuth, UserQuestion, Rate


def setup(dp: Dispatcher):
    dp.register_message_handler(user_answers.get_answer, lambda message: message.reply_to_message)
    dp.register_message_handler(user_authorization.user_authorization, filters.CommandStart())
    dp.register_message_handler(user_authorization.get_profile_panel, filters.Command("lk"))
    dp.register_callback_query_handler(kur_rate.set_rate, lambda call: call.data.startswith("r_"))
    dp.register_message_handler(kur_rate.get_rate, state=Rate.waiting_for_rate)
    dp.register_callback_query_handler(user_authorization.get_user_phone_number,
                                       lambda call: call.data == kd.AUTHORIZATION_CD)
    dp.register_callback_query_handler(user_questions.create_user_question,
                                       lambda call: call.data == kd.ASK_A_QUESTION_CD)
    dp.register_callback_query_handler(user_questions.send_user_questions,
                                       lambda call: call.data == kd.RIGHT_QUESTION_CD,
                                       state=UserQuestion.waiting_for_user_question)
    dp.register_callback_query_handler(user_questions.create_user_question,
                                       state=UserQuestion.waiting_for_user_question)
    dp.register_message_handler(user_questions.is_right_question, state=UserQuestion.waiting_for_user_question)
    dp.register_message_handler(user_authorization.check_phone, state=UserAuth.waiting_for_valid_phone)
    dp.register_message_handler(user_answers.new_question)
