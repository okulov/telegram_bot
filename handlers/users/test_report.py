import os
import pathlib

from aiogram import types

from loader import dp, bot
from aiogram.types import InputFile
from utils.get_csv_report import get_report


@dp.message_handler(text='1')
async def bot_test_report(message=types.Message):
    # get_report('amocrm_export_leads_2021-02-13.csv')
    #path_out = os.path.join(os.getcwd(), 'download\output')
    #path_out = os.path.join(path_out, 'payments2.xls')
    #cat = InputFile("/download/payments2.xls")
    #cat = InputFile(path_out)
    #print(path_in)
    await message.answer('Отправляю')
    #await bot.send_document(message.chat.id, cat)
