import re
import pytz

from datetime import datetime, timedelta
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment
from keyboards.keyboard import manager_history_cbkb

# 
async def manager_history_cb(callback: CallbackQuery, state: FSMContext, db: AsyncSession):
    match = re.search(rf"\bmhistory_(all|paid)\b", callback.data)
    if not match:
        return

    sdata = await state.get_data()
    if sdata.get("start_date") is None:
        await state.finish()
        return await callback.message.edit_text("Запрос устарел")

    if sdata.get('end_date') is None:
        data = await Payment.manager_history(db, sdata['start_date'], status=match.group(1))
    else:
        data = await Payment.manager_history(db, sdata['start_date'], sdata['end_date'], match.group(1))

    if data is None or data == []:
        try:
            return await callback.message.edit_text(
                "⛈ Нет данных",
                reply_markup=manager_history_cbkb()
            )
        except Exception:
            return await callback.answer()
    
    message_text = 'Формат: Название платежа, Сумма, Описание, Кем создано, Статус\n'
    temp_date = datetime(2099,12,1, tzinfo=pytz.utc)

    for i in data:
        if i[3].date() != temp_date.date():
            temp_date = i[3]
            message_text += '\n<b>' + temp_date.strftime("%d.%m.%Y") + '</b>\n'
        message_text += f'<code>{i[0]}</code>, {i[1]//100}.{i[1]%100}₽, <i>{i[2]}</i>, @{i[5]}, {i[4].value}\n'

    try:
        await callback.message.edit_text(message_text, reply_markup=manager_history_cbkb())
    except Exception:
        await callback.answer()

async def manager_history_periods_cb(callback: CallbackQuery, state: FSMContext, db: AsyncSession):
    match = re.search(rf"\bmperiod_history_(\d+)days\b", callback.data)
    print(callback.data, match.string)
    if not match:
        return

    end_date = datetime.now()
    start_date = (end_date - timedelta(days=int(match.group(1)))).strftime("%d-%m-%Y")

    async with state.proxy() as data:
        data["start_date"] = start_date
        data["end_date"] = end_date.strftime("%d-%m-%Y")

    sdata = await state.get_data()
    if sdata.get("username") is None:
        await state.finish()
        return await callback.message.edit_text("Запрос устарел")

    data = await Payment.manager_history(db, start_date, end_date.strftime("%d-%m-%Y"), name=sdata['username'])
    if data is None or data == []:
        try:
            return await callback.message.edit_text(
                "⛈ Нет данных\n",
                reply_markup=manager_history_cbkb()
            )
        except Exception:
            return await callback.answer()
    
    message_text = 'Формат: Название платежа, Сумма, Описание, Статус\n'
    temp_date = datetime(2099,12,1, tzinfo=pytz.utc)

    for i in data:
        if i[3].date() != temp_date.date():
            temp_date = i[3]
            message_text += '\n<b>' + temp_date.strftime("%d.%m.%Y") + '</b>\n'
        message_text += f'<code>{i[0]}</code>, {i[1]//100}.{i[1]%100}₽, <i>{i[2]}</i>, {i[4]}\n'

    try:
        await callback.message.edit_text(message_text, reply_markup=manager_history_cbkb())
    except Exception:
        await callback.answer()
