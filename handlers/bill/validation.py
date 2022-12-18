from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from states.issue_invoice import IssueInvoice
from keyboards.keyboard import validation_list
from utils.bill.generate_bill import generate_bill
from handlers.bill.start_issue_invoice_operation import start_issue_invoice_operation

#
async def validation(message: Message, state: FSMContext):
    if message.text not in validation_list:
        return await message.answer("Вариант не существует")

    if message.text == validation_list[1]:
        await IssueInvoice.lesson_type.set()
        return await start_issue_invoice_operation(message)

    sdata = await state.get_data()

    response = await generate_bill(sdata.get("description", ""), sdata.get("cost", 1))
    await message.answer(response)

    # payment_str = 'Номер заказа: ' + payment_info[0] + '\nСсылка на оплату:\n' + payment_info[1]['formUrl']
