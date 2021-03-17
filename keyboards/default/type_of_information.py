from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

type_info = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Финансы'),
        KeyboardButton(text='Контактные данные'),
        KeyboardButton(text='Назад'),
    ],
], resize_keyboard=True)