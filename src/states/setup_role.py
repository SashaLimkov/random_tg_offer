from aiogram.dispatcher.filters.state import StatesGroup, State


class Role(StatesGroup):
    secret_key = State()
