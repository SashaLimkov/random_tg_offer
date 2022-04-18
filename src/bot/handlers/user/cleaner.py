from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot


async def clean(message: types.Message, state: FSMContext):
    await bot.delete_message(
        chat_id=message.from_user.id, message_id=message.message_id
    )
    await state.finish()


async def clean_s(message: types.Message):
    await bot.delete_message(
        chat_id=message.from_user.id, message_id=message.message_id
    )
