from aiogram.dispatcher.filters.state import StatesGroup, State


class CheckBill(StatesGroup):
    parameter = State()
    parents_history_operations = State()
