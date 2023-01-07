import re
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment
from keyboards.keyboard import reset_kb
from states.check_manager import CheckManager


#
async def username(message: Message, state: FSMContext, db: AsyncSession):
    data = await Payment.check_name(db, message.text)
    if not data or data is None:
        return await message.answer("Менеджер не найден")

    async with state.proxy() as data:
        data["username"] = message.text    

    await message.answer(
        "Укажите дату, или диапазон. Формат <b>День.Месяц.Год</b>\n\n" +\
            "Пример даты: 01.01.2023\n" +\
            "Пример диапазона: 01.01.2023 10.01.2023"
    )

    await CheckManager.date.set()
