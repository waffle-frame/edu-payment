from loguru import logger
from aiogram.types import Message
from pygsheets.client import Client
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment
from states.issue_invoice import IssueInvoice
from utils.bill.generate_bill import generate_bill
from utils.spreadsheets.create_row import create_rows
from utils.spreadsheets.check_rows import check_count_rows
from handlers.bill.start_issue_invoice_operation import start_issue_invoice_operation
from keyboards.buttons import validation_list, issue_invoice_prefix
from keyboards.buttons import issue_invoice_dict

#
async def validation(message: Message, state: FSMContext, db: AsyncSession, spread_client: Client):
    if message.text not in validation_list:
        return await message.answer("Вариант не существует")

    if message.text == validation_list[1]:
        await IssueInvoice.lesson_type.set()
        return await start_issue_invoice_operation(message)

    user = message['from']
    sdata = await state.get_data()

    order_number: int | None = await Payment.create(db,
        creator_data=f"{user.id}|{user.username}",
        lesson_type=issue_invoice_dict[sdata.get("lesson_type")], parents_name=sdata.get("parents_data").title(),
        description=sdata.get("description"), amount=int(sdata.get("cost")),
    )
    if order_number is None:
        logger.error(sdata)
        return await message.answer("Упс, что-то пошло не так")

    order_id, order_link = await generate_bill(sdata["description"], sdata["cost"], order_number)
    await Payment.update(db, order_number, order_id=order_id, order_link=order_link)

    await message.answer(
        f"Счет на оплату успешно создан!\nНомер заказа: <code>{issue_invoice_prefix+issue_invoice_dict[sdata['lesson_type']]}{order_number}</code>\n" + \
        f"Ссылка на оплату: {order_link}\n\nСсылка активна в течении 2-уx недель"
    )
    await state.finish()

    # offset = await check_count_rows(db)
    offset = await check_count_rows(db, issue_invoice_dict[sdata.get("lesson_type")])
    if offset is None:
        return

    await create_rows(db, spread_client, issue_invoice_dict[sdata.get("lesson_type")], 0)
    # await create_rows(db, spread_client, "test", offset)
