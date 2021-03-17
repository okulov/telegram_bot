from aiogram import types

from loader import dp


@dp.message_handler()
async def message_auth(message: types.Message):
    await message.answer(
        'У вас нет прав для использования бота, обратитесь к администратору или в отдел маркетинга Barca Academy.')
