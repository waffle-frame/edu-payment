import re
import pytz

from datetime import datetime
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment
from keyboards.buttons import statuses
from keyboards.keyboard import manager_history_cbkb

# 
async def manager_history_period_cb(callback: CallbackQuery, state: FSMContext, db: AsyncSession):
    match = re.search(rf"\bmhistory_(all|paid)\b", callback.data)
    if not match:
        return

    sdata = await state.get_data()
    if sdata.get("start_date") is None:
        await state.finish()
        await callback.message.delete()
        return await callback.message.answer("Запрос устарел")

    if len(match.group()) == 10:
        data = await Payment.manager_history(db, sdata['username'], match.group(1), sdata['start_date'])
    else:
        data = await Payment.manager_history(db, sdata['username'], match.group(1), sdata['start_date'], sdata['end_date'])

    if data is None or data == []:
        try:
            return await callback.message.edit_text(
                "⛈ Нет данных",
                reply_markup=manager_history_cbkb()
            )
        except Exception:
            return await callback.answer()
    
    message_text = 'Формат: Название платежа, Сумма, Описание, Оплачено\n'
    temp_date = datetime(2099,12,1, tzinfo=pytz.utc)

    for i in data:
        if i[3].date() != temp_date.date():
            temp_date = i[3]
            message_text += '\n<b>' + temp_date.strftime("%d.%m.%Y") + '</b>\n'
        message_text += f'<code>{i[0]}</code>, {i[1]//100}.{i[1]%100}₽, <i>{i[2]}</i>, {statuses[i[4]]}\n'

    try:
        await callback.message.edit_text(message_text, reply_markup=manager_history_cbkb())
    except Exception:
        await callback.answer()
