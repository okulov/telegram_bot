from aiogram.dispatcher.filters.state import StatesGroup, State


class Payment_type(StatesGroup):
    Begin = State()
    Type_info = State()
    Filial = State()

class Lead_info(StatesGroup):
    Wait_name_lead = State()

class Download_type(StatesGroup):
    begin = State()
    finance_info = State()
    contact_info = State()