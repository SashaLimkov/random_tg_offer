from aiogram.dispatcher.filters.state import StatesGroup, State


class UserAuth(StatesGroup):
    waiting_for_valid_phone = State()
