import os
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile

from data.config import USERS
from keyboards.default import menu
from keyboards.inline import filials_ext
from loader import dp, bot
from states import Download_type
from utils import save_xls
from utils.amo import get_amo_contacts_data


@dp.message_handler(text='Контактные данные', state=[None, Download_type.finance_info], chat_id=USERS)
async def choise_type_contacts(message: types.Message):
    await Download_type.contact_info.set()
    await message.answer('Выберите филиал или все сделки', reply_markup=filials_ext)


@dp.callback_query_handler(state=Download_type.contact_info)
async def get_contact_info(call: CallbackQuery):
    await bot.answer_callback_query(text='Запрашиваю данные', callback_query_id=call.id)
    path_out = os.path.join(os.getcwd(), 'download/output')
    name_file = ''.join(['Contacts_', call.data, '_', datetime.now().strftime("%d_%m_%y_%H_%M"), '.xls'])
    file_out = os.path.join(path_out, name_file)
    await call.message.answer('Сбор данных по контактам может занять до минуты, подождите, бот работает.')
    list_contacts = get_amo_contacts_data(query=call.data)
    save_xls(list_contacts, file_out)
    cat = InputFile(file_out)
    await bot.send_document(call.message.chat.id, cat, caption=f'Отчет готов.')


@dp.message_handler(text='Назад', state=Download_type.contact_info)
async def back_button_contact(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Выберите действие:', reply_markup=menu)
