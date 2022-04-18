from aiogram import Dispatcher
from bot.handlers import user, admin


def setup(dp: Dispatcher):
    user.setup(dp)
