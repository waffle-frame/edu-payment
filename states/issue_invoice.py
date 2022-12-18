from aiogram.dispatcher.filters.state import StatesGroup, State


class IssueInvoice(StatesGroup):
    lesson_type = State()
    parents_data = State()
    description = State()
    cost = State()
    validation = State()
