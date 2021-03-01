from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! \nЭтот бот работает с отчетами AMO."
        f"\nМожет обрабатывать как выгрузки CSV, так и самостоятельно запрашивать данные из AMO CRM.", reply_markup=menu)

