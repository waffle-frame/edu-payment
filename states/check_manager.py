from aiogram.dispatcher.filters.state import StatesGroup, State


class CheckManager(StatesGroup):
    parameter = State()
    username = State()
    username_date = State()
    date = State()
