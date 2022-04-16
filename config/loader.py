from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

from config.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
user_data = {}
kurators_state={}

base = sqlite3.connect('table.db')
cur = base.cursor()

base.execute(
    'CREATE TABLE IF NOT EXISTS {}(id PRIMARY KEY,number,role,state,state2,kurmes,nastmes)'.format(
        'data'))
base.commit()