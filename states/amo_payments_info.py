from aiogram.dispatcher.filters.state import StatesGroup, State


class Payment_type(StatesGroup):
    Type_info = State()
    Filial = State()