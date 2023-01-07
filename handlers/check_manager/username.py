import re
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment
from states.check_manager import CheckManager
from keyboards.keyboard import manager_history_periods_cbkb, manager_history_cbkb


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
        "Пример диапазона: 01.01.2023 10.01.2023",
        reply_markup=manager_history_periods_cbkb()
    )

async def username_period(message: Message, state: FSMContext, db: AsyncSession):
    regex = r"(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d"

    match = re.search(rf"({regex})? ?{regex}", message.text)
    if not bool(match):
        return await message.answer(
            "Не корректный формат\n" +\
            "Пример даты: 01.01.2023\n" +\
            "Пример диапазона: 01.01.2023 07.01.2023", 
            reply_markup=manager_history_periods_cbkb()
        )

    await message.answer("Выберите операцию:", reply_markup=manager_history_cbkb())
