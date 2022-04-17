from aiogram.dispatcher.filters.state import StatesGroup, State


class Rate(StatesGroup):
    waiting_for_rate = State()
