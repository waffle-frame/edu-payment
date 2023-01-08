import re
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from states.issue_invoice import IssueInvoice
from keyboards.keyboard import reset_kb


#
async def parents_data(message: Message, state: FSMContext):
    if len(message.text.split(" ")) != 2:
        return await message.answer("Введите полное <b>Фамилию</b> и <b>Имя</b> родителя\nНапример: Григорьев Александр")

    if not bool(re.search("[А-Яа-я]{2}", message.text)):
        return await message.answer("⚠️ Вводите только в кириллице")

    async with state.proxy() as data:
        data["parents_data"] = message.text.title()

    await message.answer("Введите описание:", reply_markup=reset_kb())
    await IssueInvoice.description.set()
