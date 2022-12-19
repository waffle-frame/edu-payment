from loguru import logger
from aiogram.types import Message
from sqlalchemy.orm import scoped_session
from aiogram.dispatcher import FSMContext

from models.payment import Payment
from states.issue_invoice import IssueInvoice
from utils.bill.generate_bill import generate_bill
from keyboards.keyboard import validation_list, issue_invoice_dict
from handlers.bill.start_issue_invoice_operation import start_issue_invoice_operation


#
async def validation(message: Message, state: FSMContext, db: scoped_session):
    if message.text not in validation_list:
        return await message.answer("Вариант не существует")

    if message.text == validation_list[1]:
        await IssueInvoice.lesson_type.set()
        return await start_issue_invoice_operation(message)

    user = message['from']
    sdata = await state.get_data()

    order_number: int | None = await Payment.create(db,
        creator_data=f"{user.id}|{user.username}",
        lesson_type=sdata.get("lesson_type"), parents_name=sdata.get("parents_data"),
        description=sdata.get("description"), amount=int(sdata.get("cost")),
    )
    if order_number is None:
        logger.error(sdata)
        return await message.answer("Упс, что-то пошло не так")

    order_id, order_link = await generate_bill(sdata["description"], sdata["cost"], order_number)
    await Payment.update(db, order_number, order_id=order_id, order_link=order_link)

    await message.answer(
        f"Счет на оплату успешно создан!\nНомер заказа: <code>{issue_invoice_dict[sdata['lesson_type']]}{order_number}</code>\n" + \
        f"Ссылка на оплату: {order_link}\n\nСсылка активна в течении 2-уx недель"
    )
