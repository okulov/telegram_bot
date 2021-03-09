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
                                           text='Оба',
                                           callback_data='all'
                                       )
                                   ]
                               ])

report_xls = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                                  text = 'Скачать отчет XLS',
                                                  callback_data='download_xls'
                                          )
                                      ]
                                  ])