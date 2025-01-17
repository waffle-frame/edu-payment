from aiogram.types import Message

from states.issue_invoice import IssueInvoice
from keyboards.keyboard import operations_kb, issue_invoice_kb
from keyboards.buttons import operations_list, validation_list


# Start the billing process. List of available type lessons
async def start_issue_invoice_operation(message: Message):
    if (message.text not in operations_list) and message.text != '/invoice':
        await message.answer("Вариант не существует")
        return await message.answer("Выберите операцию:", reply_markup=operations_kb())

    await message.answer("Выберите тип занятия:", reply_markup=issue_invoice_kb())
    await IssueInvoice.lesson_type.set()
