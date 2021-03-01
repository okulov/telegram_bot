import os
from datetime import datetime

from aiogram import types
from aiogram.types import CallbackQuery, InputFile

from keyboards.default import menu
from keyboards.inline.filials_buttons import filials
from loader import dp, bot
from utils.amo import get_report


@dp.message_handler(text='Выгрузить из AMO')
async def choise_filials(message: types.Message):
    await message.answer(text='Выберите филиал или сразу оба:', reply_markup=filials)


@dp.message_handler(text='Обработать файл')
async def answer_about_files(message: types.Message):
    await message.answer(
        text='Просто кидайте нужный файл боту и он обработает его. В ответ он вышлет вам итоговый файл.',
        reply_markup=menu)


@dp.callback_query_handler()
async def get_reports(call: CallbackQuery):
    # await call.answer(text=call.data)
    await bot.answer_callback_query(text=call.data, callback_query_id=call.id)
    name_filial = str('филиал ' + call.data) if call.data != 'all' else "оба филиала"
    await call.message.answer(
        f'Вы выбрали {name_filial}. Пока работаем только с воронкой "Школа" и статусом "Получена оплата".')
    await call.message.answer('Скачиваю данные из АМО...')

    path_out = os.path.join(os.getcwd(), 'download/output')
    file_out = os.path.join(path_out, ''.join(['payments_', str(datetime.now().date()), '.xls']))

    amount_id = get_report(call.data, file_out)
    cat = InputFile(file_out)
    await bot.send_document(call.message.chat.id, cat, caption=f'Отчет готов.\nУникальных id сделок: {amount_id}')
