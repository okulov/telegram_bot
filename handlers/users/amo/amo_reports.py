import os
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile

from keyboards.default import menu
from keyboards.inline import filials
from loader import dp, bot
from states import Download_type
from utils.amo import get_amo_payments_data


@dp.message_handler(text='Финансы', state=[None, Download_type.contact_info, Download_type.finance_info])
async def choise_filials(message: types.Message, state: FSMContext):
    await Download_type.finance_info.set()
    await message.answer(text='Выберите филиал или сразу оба:', reply_markup=filials)

@dp.callback_query_handler(state=Download_type.finance_info)
async def get_reports(call: CallbackQuery):
    await bot.answer_callback_query(text='Формирую отчет...', callback_query_id=call.id)
    name_filial = str('филиал ' + call.data) if call.data != 'all' else "оба филиала"
    await call.message.answer(
        f'Вы выбрали {name_filial}. Пока работаем только с воронкой "Школа" и статусом "Получена оплата".')
    await call.message.answer('Скачиваю данные из АМО...')

    path_out = os.path.join(os.getcwd(), 'download/output')
    file_out = os.path.join(path_out, ''.join(['payments_', name_filial, '_', str(datetime.now().date()), '.xls']))

    amount_id = get_amo_payments_data(call.data, file_out=file_out, method_out='file')
    cat = InputFile(file_out)
    await bot.send_document(call.message.chat.id, cat, caption=f'Отчет готов.\nУникальных id сделок: {amount_id}')

@dp.message_handler(text = 'Назад', state=Download_type.finance_info)
async def back_button_finance(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Выберите действие:', reply_markup=menu)