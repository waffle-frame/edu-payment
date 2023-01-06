import pytz

from datetime import datetime
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment
from states.check_bill import CheckBill
from keyboards.buttons import parent_history_operations_list
from keyboards.keyboard import parents_history_operations_kb, parents_history_cbkb


#
async def parents_history_operations(message: Message, state: FSMContext, db: AsyncSession):
    if message.text == parent_history_operations_list[0]:
        sdata = await state.get_data()
        data = await Payment.paid_invoice(db, sdata['parents_name'])
        if data is None or data == []:
            return await message.answer("⛈ Оплаченные заказы отсутствуют")

        message_text = 'Формат: Название платежа, Сумма\n'
        temp_date = datetime(2099,12,1, tzinfo=pytz.utc)
        for i in data:
            if i[2].date() != temp_date.date():
                temp_date = i[2]
                message_text += '\n<b>' + temp_date.strftime("%d.%m.%Y") + '</b>\n'
            message_text += f'{i[0]}, {i[1]//100}.{i[1]%100}₽\n'

        return await message.answer(message_text)

    if message.text == parent_history_operations_list[1]:
        return await message.answer("Выберите диапазон:", reply_markup=parents_history_cbkb())

    await message.answer("Вариант не существует")
    await message.answer("Выберите операцию:", reply_markup=parents_history_operations_kb())
