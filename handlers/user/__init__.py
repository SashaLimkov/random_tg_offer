from aiogram import Dispatcher
from aiogram.dispatcher import filters

from data import keyboards_data as kd
from handlers.user import echo, user_authorization
from states import UserAuth


def setup(dp: Dispatcher):
    dp.register_message_handler(user_authorization.user_authorization, filters.CommandStart())
    dp.register_callback_query_handler(user_authorization.get_user_phone_number,
                                       lambda call: call.data == kd.AUTHORIZATION)
    dp.register_message_handler(user_authorization.check_phone, state=UserAuth.waiting_for_valid_phone)
    dp.register_message_handler(echo.echo_message)
