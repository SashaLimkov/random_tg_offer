from aiogram import Dispatcher
from handlers import user, admin


def setup(dp: Dispatcher):
    user.setup(dp)
