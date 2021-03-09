import os
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile

from keyboards.default import menu
from keyboards.inline.filials_buttons import filials, report_xls
from loader import dp, bot
from states.amo_payments_info import Payment_type
from utils.amo import get_amo_data, get_summary_info
from utils.get_csv_report import save_xls


@dp.message_handler(text=['Общая информация', 'Текущий месяц', 'Прошлый месяц'],
                    state=[None, Payment_type.Type_info, Payment_type.Filial])
async def choice_type_info(message: types.Message, state: FSMContext):
    await Payment_type.Type_info.set()
    await state.update_data(type_info=message.text)
    await message.answer(text='Выберите филиал или сразу оба:', reply_markup=filials)


@dp.callback_query_handler(state=Payment_type.Type_info)
async def get_payments_info(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(text='Идет запрос информации...', callback_query_id=call.id)
    data_state = await state.get_data()
    type_info = data_state.get('type_info')
    filial = call.data

    data_amo = get_amo_data(filial, method_out='dict')
    data_payments = get_summary_info(data_amo, filial=filial, type=type_info)
    await Payment_type.Filial.set()
    await state.update_data(info_xls=data_payments.get('data'))
    await state.update_data(filial=filial)
    await call.message.answer(data_payments.get('info'), reply_markup=report_xls)


@dp.callback_query_handler(state=Payment_type.Filial)
async def download_info_xls(call: CallbackQuery, state: FSMContext):
    path_out = os.path.join(os.getcwd(), 'download/output')
    data_state = await state.get_data()
    file_out = os.path.join(path_out,
                            ''.join(['Report_', data_state.get('filial'), '_', str(datetime.now()), '.xls']))
    save_xls(data_state.get('info_xls'), file_out)
    # amount_id = get_amo_data(call.data, file_out=file_out, method_out='file')
    cat = InputFile(file_out)
    await bot.send_document(call.message.chat.id, cat, caption=f'Отчет готов.')


@dp.message_handler(text='Назад', state=[None, Payment_type.Type_info, Payment_type.Filial])
async def back_button(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Выберите действие:', reply_markup=menu)
