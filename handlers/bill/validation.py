from loguru import logger
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment
from states.issue_invoice import IssueInvoice
from utils.bill.generate_bill import generate_bill
from handlers.bill.start_issue_invoice_operation import start_issue_invoice_operation
from keyboards.buttons import validation_list, issue_invoice_prefix, issue_invoice_dict
from keyboards.keyboard import operations_kb

#
async def validation(message: Message, state: FSMContext, db: AsyncSession):
    if message.text not in validation_list:
        return await message.answer("Вариант не существует")

    if message.text == validation_list[1]:
        await IssueInvoice.lesson_type.set()
        return await start_issue_invoice_operation(message)

    user = message['from']
    sdata = await state.get_data()

    row, id = await Payment.create(db,
        creator_username=user.username,
        creator_telegram_id=user.id,
        parents_name=sdata.get("parents_data"),

        lesson_type=issue_invoice_dict[sdata.get("lesson_type", 'test')],
        description=sdata.get("description"), 
        amount=int(sdata.get("cost", 0)),
    )
    if id is None or row is None:
        logger.error(sdata)
        return await message.answer("⚠️ Упс, что-то пошло не так")

    order = issue_invoice_prefix+issue_invoice_dict[sdata['lesson_type']]

    order_id, order_link = await generate_bill(sdata["description"], sdata["cost"], order)
    if order_id == "" or order_link == "":
        return await message.answer("Сумма не должна превышать 42949672.95 рублей")

    print(order_id, order_link)

    await Payment.update(db, id, order_id=order_id, order_link=order_link)

    await message.answer(
        f"Счет на оплату успешно создан!\nНомер заказа: <code>{order}{row-1}</code>\n" + \
        f"Ссылка на оплату: {order_link}\n\nСсылка активна в течении 2-уx недель", reply_markup=operations_kb()
    )
    await state.finish()
