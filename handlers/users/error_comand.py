from aiogram import types

from data.config import USERS
from loader import dp


@dp.message_handler(chat_id=USERS)
async def message_auth(message: types.Message):
    await message.answer(
        'Не корректная команда, нажмите "Назад" или перезагрузите бота командой /start \nЕсли ничего не помогло, обратитесь к администратору.')
