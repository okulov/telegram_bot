from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default import menu
from keyboards.inline.filials_buttons import filials
from loader import dp, bot
from states.amo_payments_info import Payment_type
from utils.amo import get_amo_data, get_summary_info


@dp.message_handler(text=['Общая информация', 'Текущий месяц', 'Прошлый месяц'], state=[None, Payment_type.Type_info])
async def choice_type_info(message: types.Message, state: FSMContext):
    await Payment_type.Type_info.set()
    await state.update_data(type_info=message.text)
    await message.answer(text='Выберите филиал или сразу оба:', reply_markup=filials)


@dp.callback_query_handler(state=Payment_type.Type_info)
async def get_payments_info(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(text='Идет запрос информации...', callback_query_id=call.id)
    type = await state.get_data()
    type_info = type.get('type_info')
    filial = call.data
    data_amo = get_amo_data(filial, method_out='dict')
    data_payments = get_summary_info(data_amo, filial = filial, type=type_info)
    await call.message.answer(data_payments)


@dp.message_handler(text='Назад', state=[None, Payment_type.Type_info])
async def back_button(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Выберите действие:', reply_markup=menu)
