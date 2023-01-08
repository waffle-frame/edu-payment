import re
import pytz

from datetime import datetime
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment
from keyboards.keyboard import manager_history_cbkb
from states.check_manager import CheckManager


#
async def date(message: Message, state: FSMContext, db: AsyncSession):
    regex = r"(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d"

    match = re.search(rf"({regex})? ?{regex}", message.text)
    if not bool(match):
        return await message.answer(
            "Не корректный формат\n" +\
            "Пример даты: 01.01.2023\n" +\
            "Пример диапазона: 01.01.2023 07.01.2023"
        )

    async with state.proxy() as data:
        match = match.string.split(' ')
        if len(match) == 2:
            data["start_date"] = match[0].replace(".", "-")
            data["end_date"] = match[1].replace(".", "-")
        else:
            data["start_date"] = match[0].replace(".", "-")
            data["end_date"] = None

    await message.answer("Выберите операцию:", reply_markup=manager_history_cbkb())