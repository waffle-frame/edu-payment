import re

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.check_manager import CheckManager
from keyboards.buttons import manager_history_operations_list
from keyboards.keyboard import manager_history_date_range_operations_kb, \
    manager_history_operations_kb

#
async def manager_username_or_date(message: Message):
    if message.text == manager_history_operations_list[0]:
        await CheckManager.username.set()
        return await message.answer(
            "Укажите <b>username</b> менеджера",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Я")]], resize_keyboard=True)
        )

    if message.text == manager_history_operations_list[1]:
        await CheckManager.daterange.set()
        return await message.answer(
            "Выберите свойства поиска:",
            reply_markup=manager_history_date_range_operations_kb(),
        )

    return await message.answer("Неизвестная комбинация. Повторите попытку", reply_markup=manager_history_operations_kb())
