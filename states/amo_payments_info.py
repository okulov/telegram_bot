from aiogram.dispatcher.filters.state import StatesGroup, State


class Payment_type(StatesGroup):
    Type_info = State()
    Filial = State()

class Lead_info(StatesGroup):
    Wait_name_lead = State()

class Download_type(StatesGroup):
    finance_info = State()
    contact_info = State()