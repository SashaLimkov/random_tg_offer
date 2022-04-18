import os

import aiogram
import django
from aiogram import Dispatcher, types
from django.conf import settings
from django.core.management import BaseCommand

from bot import handlers
from bot.config.loader import dp


async def on_startup(*args, **kwargs):
    handlers.setup(dp)
    print("Bot started!")


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegrambot.settings")
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


def start_bot(*args, **kwargs):
    setup_django()
    aiogram.executor.start_polling(
        dp, on_startup=on_startup, on_shutdown=shutdown, skip_updates=False
    )


class Command(BaseCommand):
    help = "Start bot"

    def handle(self, *args, **options):
        start_bot()
