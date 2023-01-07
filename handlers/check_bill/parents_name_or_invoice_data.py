import re

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment
from states.check_bill import CheckBill
from keyboards.keyboard import parents_history_operations_kb
from keyboards.buttons import issue_invoice_prefix, issue_invoice_dict

#
async def parents_name_or_invoice_data(message: Message, state: FSMContext, db: AsyncSession):
    if len(message.text) < 4:
        return await message.answer("Неизвестная комбинация. Повторите попытку")

    if message.text[0:4] == issue_invoice_prefix:
        match = re.search(rf"({'|'.join(issue_invoice_dict.values())})(\d+)", message.text[3:])
        if not bool(match):
            return await message.answer("Неверный номер заказа. Повторите попытку")

        order_info = await Payment.check_invoice(db, int(match.group(2)), match.group(1))
        if order_info is None:
            return await message.answer("Данные по номеру заказа не найдены")

        await state.finish()
        return await message.answer(
            f"Статус: {order_info[0]}\n" +
            f"Создан: {order_info[1].strftime('%d.%m.%Y %H:%m')}\n" + 
            f"Владелец: @{order_info[2]}"
        )

    if len(message.text.split(" ")) != 2:
        return await message.answer(
            "Введите полное <b>Фамилию</b> и <b>Имя</b> родителя в указанном порядке"
        )

    if not bool(re.search("[А-Яа-я]{2}", message.text)):
        return await message.answer("⚠️ Вводите только в кириллице")

    is_founded = await Payment.check_name(db, message.text)
    if is_founded is None:
        await state.finish()
        return message.answer("Родитель не найден")

    async with state.proxy() as data:
        data["parents_name"] = message.text.title()


    await CheckBill.parents_history_operations.set()
    await message.answer("Выберите операцию:", reply_markup=parents_history_operations_kb())
