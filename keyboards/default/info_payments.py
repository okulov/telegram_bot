from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

info_payments = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Общая информация'),
        KeyboardButton(text='Текущий месяц'),
    ], [
        KeyboardButton(text='Прошлый месяц'),
        KeyboardButton(text='Назад'),

    ]
], resize_keyboard=True)
