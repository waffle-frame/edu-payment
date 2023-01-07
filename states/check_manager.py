from aiogram.dispatcher.filters.state import StatesGroup, State


class CheckManager(StatesGroup):
    username = State()
    parents_history_operations = State()
    date = State()
