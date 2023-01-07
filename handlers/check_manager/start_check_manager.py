import re
from aiogram.types import Message

from keyboards.keyboard import manager_history_operations_kb
from states.check_manager import CheckManager


#
async def start_check_manager(message: Message):
    await message.answer("Для отмены введите команду /cancel")
    await message.answer(
        "Осуществить поиск:",
        reply_markup=manager_history_operations_kb(),
    )

    await CheckManager.parameter.set()
