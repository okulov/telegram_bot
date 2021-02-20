from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! \nЭтот бот может делать отчет на основе высланного "
        f"ему отчета из АМО. Просто киньте в чат сам файл и он вышлет обратно файл отчета")
