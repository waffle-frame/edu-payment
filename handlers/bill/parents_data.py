import re
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from states.issue_invoice import IssueInvoice
from keyboards.buttons import go_back
from keyboards.keyboard import go_back_kb
from handlers.bill.start_issue_invoice_operation import start_issue_invoice_operation


#
async def parents_data(message: Message, state: FSMContext):
    if message.text == go_back:
        message.text = "/invoice"
        return await start_issue_invoice_operation(message)

    if len(message.text.split(" ")) != 2:
        return await message.answer("Введите полное <b>Фамилию</b> и <b>Имя</b> родителя\nНапример: Григорьев Александр")

    if not bool(re.search("[А-Яа-я]{2}", message.text)):
        return await message.answer("⚠️ Вводите только в кириллице")

    async with state.proxy() as data:
        data["parents_data"] = message.text.title()

    await message.answer("Введите описание:", reply_markup=go_back_kb())
    await IssueInvoice.description.set()
