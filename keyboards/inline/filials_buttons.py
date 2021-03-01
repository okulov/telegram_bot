from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

filials = InlineKeyboardMarkup(row_width=3,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(
                                           text='Ходынка',
                                           callback_data='Ходынка'
                                       ),
                                       InlineKeyboardButton(
                                           text='Рига',
                                           callback_data='Рига'
                                       ),
                                       InlineKeyboardButton(
                                           text='Оба филиала',
                                           callback_data='all'
                                       )
                                   ]
                               ])
