import re
from aiogram.types import Message

from states.check_bill import CheckBill
from keyboards.keyboard import reset_kb


#
async def start_check_bill(message: Message):
    await message.answer("Для отмены введите команду /cancel")
    await message.answer(
        "Укажите <b>Фамилию</b> и <b>Имя</b> родителя в указанном порядке или номер заказа:", 
        reply_markup=reset_kb(),
    )

    await CheckBill.parameter.set()
