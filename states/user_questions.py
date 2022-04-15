from aiogram.dispatcher.filters.state import StatesGroup, State


class UserQuestion(StatesGroup):
    waiting_for_user_question = State()
    waiting_for_answer = State()
