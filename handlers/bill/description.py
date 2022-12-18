from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from states.issue_invoice import IssueInvoice
from keyboards.keyboard import reset_kb


# 
async def description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text

    await message.answer("Введите сумму в копейках:", reply_markup=reset_kb())
    await IssueInvoice.cost.set()
