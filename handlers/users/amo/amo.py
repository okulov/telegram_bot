from aiogram import types

from keyboards.default import menu, info_payments, back
from keyboards.inline import filials
from loader import dp
from states import Lead_info


@dp.message_handler(text='Выгрузить из AMO')
async def choise_filials(message: types.Message):
    await message.answer(text='Выберите филиал или сразу оба:', reply_markup=filials)


@dp.message_handler(text='Обработать файл')
async def answer_about_files(message: types.Message):
    await message.answer(
        text='Просто кидайте нужный файл боту и он обработает его. В ответ он вышлет вам итоговый файл.',
        reply_markup=menu)

@dp.message_handler(text='Информация по оплатам')
async def change_main_buttons(message: types.Message):
    await message.answer(
        text='Выберите, что хотите видеть по суммарной информации об оплатах?',
        reply_markup=info_payments)

@dp.message_handler(text='Запрос по клиенту')
async def request_lead_info(message: types.Message):
    await message.answer(text='Введите ID сделки или ее наименование (фамилия клиента):', reply_markup=back)
    await Lead_info.Wait_name_lead.set()






