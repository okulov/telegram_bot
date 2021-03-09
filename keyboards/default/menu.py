from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Обработать файл'),
        KeyboardButton(text='Выгрузить из AMO'),
    ], [
        KeyboardButton(text='Информация по оплатам'),
        KeyboardButton(text='Запрос по клиенту'),

    ]
], resize_keyboard=True)

back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Назад'),
    ]
], resize_keyboard=True)