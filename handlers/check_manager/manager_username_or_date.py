import re

from aiogram.types import Message

from states.check_manager import CheckManager
from keyboards.buttons import manager_history_operations_list
from keyboards.keyboard import manager_history_operations_kb, reset_kb

#
async def manager_username_or_date(message: Message):
    if message.text == manager_history_operations_list[0]:
        await CheckManager.username.set()
        return await message.answer("Укажите <b>username</b> менеджера", reply_markup=reset_kb())

    if message.text == manager_history_operations_list[1]:
        await CheckManager.date.set()
        return await message.answer(
            "Дату или диапазон\n\n" +\
            "Пример даты: 01.01.2023\n" +\
            "Пример диапазона: 01.01.2023 10.01.2023",
            reply_markup=reset_kb()
        )

    return await message.answer("Неизвестная комбинация. Повторите попытку", reply_markup=manager_history_operations_kb())
