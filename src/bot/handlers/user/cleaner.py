from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot, mes_to_del


async def clean(message: types.Message, state: FSMContext):
    await bot.delete_message(
        chat_id=message.from_user.id, message_id=message.message_id
    )
    await state.finish()


async def clean_s(message: types.Message):
    await bot.delete_message(
        chat_id=message.from_user.id, message_id=message.message_id
    )


async def del_mes_history(user_id):
    try:
        for mes in mes_to_del[user_id]:
            try:
                await bot.delete_message(
                    chat_id=user_id,
                    message_id=mes
                )
            except Exception as e:
                print(e)
                print(f"{user_id} не получилось удалить сообщение {mes}")
    except:
        print(f"у юзера {user_id} нет сообщений для удаления")
