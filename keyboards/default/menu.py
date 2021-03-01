from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Обработать файл'),
        KeyboardButton(text='Выгрузить из AMO'),

    ]
], resize_keyboard=True)