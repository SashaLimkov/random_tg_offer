from aiogram import Dispatcher
from src.bot.handlers import user


def setup(dp: Dispatcher):
    user.setup(dp)
