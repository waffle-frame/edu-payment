from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from handlers.base. go_to import go_to_menu
from states.issue_invoice import IssueInvoice
from keyboards.buttons import issue_invoice_dict, go_back
from keyboards.keyboard import issue_invoice_kb, go_back_kb

# 
async def lesson_type(message: Message, state: FSMContext):
    if message.text == go_back:
        message.text = "/invoice"
        return await go_to_menu(message, state)

    if message.text not in issue_invoice_dict.keys():
        await message.answer("Вариант не существует")
        return await message.answer("Выберите тип занятия:", reply_markup=issue_invoice_kb())

    async with state.proxy() as data:
        data["lesson_type"] = message.text

    await message.answer(
        "Введите <b>Фамилию</b> и <b>Имя</b> родителя\n" + \
        "⚠️ Внимание введите данные в указанном порядке:", 
        reply_markup=go_back_kb()
    )

    await IssueInvoice.parents_data.set()
