import re
from aiogram.types import Message

from keyboards.keyboard import reset_kb
from states.check_manager import CheckManager


#
async def start_check_manager(message: Message):
    await message.answer("Для отмены введите команду /cancel")
    await message.answer(
        "Укажите <b>username</b> менеджера:", 
        reply_markup=reset_kb(),
    )

    await CheckManager.username.set()
