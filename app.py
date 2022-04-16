from aiogram import Dispatcher
from aiogram.utils import executor

from src.bot import handlers
from src.bot.config.loader import dp


async def on_startup(dispatcher: Dispatcher):
    handlers.setup(dispatcher)


async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    executor.start_polling(
        dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=False
    )
