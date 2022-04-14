from aiogram import types

from config import config
from config.loader import bot, cur


async def create_user_questions(message: types.Message):
    us_id = message.from_user.id
    user_state = int(cur.execute('SELECT state FROM data WHERE id == ?', (us_id,)).fetchone()[0])
    role = int(cur.execute('SELECT role FROM data WHERE id == ?', (us_id,)).fetchone()[0])
    number = int(cur.execute('SELECT number FROM data WHERE id == ?', (us_id,)).fetchone()[0])

    if role == 'ученик' and user_state == 1 :
        await bot.send_message(us_id, "Ваш вопросы был направлен куратору, пожалуйста, ожидайте ответа",)
        await bot.send_message(config.CHANNEL_KURATOR,
                                               f'{us_id}\nНомер пользователя: {number}\n\nВопрос: {message.text}')
        await bot.send_message(config.CHANNEL_NASTAVNIK,
                                               f'{us_id}\nНомер пользователя: {number}\n\nВопрос: {message.text}')
