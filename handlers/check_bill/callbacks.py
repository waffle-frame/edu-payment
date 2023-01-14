import re
import pytz

from datetime import datetime
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment
from keyboards.keyboard import parents_history_cbkb, \
    manager_history_operations_kb

# 
async def parents_history_days_cb(callback: CallbackQuery, state: FSMContext, db: AsyncSession):
    match = re.search(rf"\bphistory_(\d+)days\b", callback.data)
    if not match:
        return

    # data = await Payment.parents_history(db, "Фыв Фыв", int(match.group(1)))
    sdata = await state.get_data()
    if sdata.get('parents_name') is None:
        await state.finish()
        await callback.message.edit_caption("Запрос устарел")
        return await callback.message.answer("Выберите операцию:", reply_markup=manager_history_operations_kb())

    data = await Payment.parents_history(db, sdata['parents_name'], int(match.group(1)))
    if data is None or data == []:
        try:
            return await callback.message.edit_text(
                "⛈ Родитель не совершал оплату", 
                reply_markup=parents_history_cbkb()
            )
        except Exception:
            return await callback.answer()

    message_text = 'Формат: Название платежа, Сумма, Описание, Кем создан, Статус\n'
    temp_date = datetime(2099,12,1, tzinfo=pytz.utc)

    for i in data:
        if i[3].date() != temp_date.date():
            temp_date = i[3]
            message_text += '\n<b>' + temp_date.strftime("%d.%m.%Y") + '</b>\n'
        message_text += f'<code>{i[0]}</code>, {i[1]//100}.{i[1]%100}₽, <i>{i[2]}</i>, @{i[4]}, {i[5]}\n'

    try:
        await callback.message.edit_text(message_text, reply_markup=parents_history_cbkb())
    except Exception:
        await callback.answer()
