from aiogram import types
from aiogram.dispatcher import filters

from data.config import USERS
from keyboards.default import menu, info_payments, back, type_info
from keyboards.inline import filials
from loader import dp
from states import Lead_info, Payment_type, Download_type


@dp.message_handler(text='Выгрузить из AMO', chat_id=USERS)
async def choise_tupe_information(message: types.Message):
    await Download_type.begin.set()
    await message.answer(text='Какую информацию выгрузить?', reply_markup=type_info)


@dp.message_handler(text='Обработать файл', chat_id=USERS)
async def answer_about_files(message: types.Message):
    await message.answer(
        text='Просто кидайте нужный файл боту и он обработает его. В ответ он вышлет вам итоговый файл.',
        reply_markup=menu)


#@dp.message_handler(chat_id=USERS)
#dp.message_handler(filters.IDFilter(chat_id=USERS))
@dp.message_handler(text='Информация по оплатам', chat_id=USERS)
async def change_main_buttons(message: types.Message):
    await Payment_type.Begin.set()
    await message.answer(
        text='Выберите, что хотите видеть по суммарной информации об оплатах?',
        reply_markup=info_payments)

#@dp.message_handler(filters.IDFilter(chat_id=USERS))
@dp.message_handler(text='Запрос по клиенту', chat_id=USERS)
async def request_lead_info(message: types.Message):
    await message.answer(text='Введите ID сделки или ее наименование (фамилия клиента):', reply_markup=back)
    await Lead_info.Wait_name_lead.set()






