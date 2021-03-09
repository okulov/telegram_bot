import os
from datetime import datetime

from aiogram.types import CallbackQuery, InputFile

from loader import dp, bot
from utils.amo import get_amo_data


@dp.callback_query_handler()
async def get_reports(call: CallbackQuery):
    # await call.answer(text=call.data)
    await bot.answer_callback_query(text=call.data, callback_query_id=call.id)
    name_filial = str('филиал ' + call.data) if call.data != 'all' else "оба филиала"
    await call.message.answer(
        f'Вы выбрали {name_filial}. Пока работаем только с воронкой "Школа" и статусом "Получена оплата".')
    await call.message.answer('Скачиваю данные из АМО...')

    path_out = os.path.join(os.getcwd(), 'download/output')
    file_out = os.path.join(path_out, ''.join(['payments_', name_filial, '_', str(datetime.now().date()), '.xls']))

    print(file_out)
    amount_id = get_amo_data(call.data, file_out=file_out, method_out='file')
    cat = InputFile(file_out)
    await bot.send_document(call.message.chat.id, cat, caption=f'Отчет готов.\nУникальных id сделок: {amount_id}')