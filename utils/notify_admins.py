import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)

async def on_use_notify(dp: Dispatcher, user:str):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, f"Бот Запущен пользователем: {user}")

        except Exception as err:
            logging.exception(err)