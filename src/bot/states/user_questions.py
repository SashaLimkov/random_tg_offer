from aiogram.dispatcher.filters.state import StatesGroup, State


class UserQuestion(StatesGroup):
    waiting_for_user_question = State()
    waiting_for_new_question = State()
    waiting_for_answer = State()
    wait_for_new_q_or_done = State()
