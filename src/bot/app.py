import os

import django
from aiogram import Dispatcher
from aiogram.utils import executor
from django.conf import settings

import handlers
from config.loader import dp


async def on_startup(dispatcher: Dispatcher):
    handlers.setup(dispatcher)


async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegrambot.settings")
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    settings.configure("telegrambot.settings")
    django.setup()


if __name__ == "__main__":
    setup_django()
    executor.start_polling(
        dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=False
    )
