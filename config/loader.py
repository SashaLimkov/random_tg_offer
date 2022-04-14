from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

from config.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
user_data = {}

base = sqlite3.connect('table.db')
cur = base.cursor()

base.execute(
    'CREATE TABLE IF NOT EXISTS {}(id PRIMARY KEY,number,role,state,state2)'.format(
        'data'))
base.commit()
