from datetime import datetime
import os

from aiogram import types

from loader import dp, bot
from aiogram.types import InputFile
from utils.get_csv_report import get_report

@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def bot_file(message=types.Message):
    document_id = message.document.file_id
    file_info = await bot.get_file(document_id)
    fi = file_info.file_path
    name = message.document.file_name
    await message.answer(f'Передан файл с именем: {name}')

    if not os.path.exists('download'):
        os.mkdir('download')
    if not os.path.exists('download/input'):
        os.mkdir('download/input')
    if not os.path.exists('download/output'):
        os.mkdir('download/output')

    path_out = os.path.join(os.getcwd(), 'download\output')
    file_out = os.path.join(path_out, ''.join(['payments_',str(datetime.now().date()),'.xls']))
    path_in = os.path.join(os.getcwd(), 'download\input')
    file_in = os.path.join(path_in, name)

    await bot.download_file(fi, destination=file_in)


    await bot.send_message(message.from_user.id, 'Файл успешно получен. Формирую отчет...')

    amount_id = get_report(file_in, file_out)
    cat = InputFile(file_out)
    await bot.send_document(message.chat.id, cat, caption=f'Отчет готов.\nУникальных id сделок: {len(set(amount_id))}'
                                                          f'\nСтрок в отчете: {len(amount_id)}')
