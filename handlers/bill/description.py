from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.keyboard import reset_kb
from states.issue_invoice import IssueInvoice


# 
async def description(message: Message, state: FSMContext):
    if len(message.text) > 512:
        return message.answer(
            f"Текст описания не должно превышать 512 символов\nСодержание вашего сообщения:{len(message.text)}"
        )

    async with state.proxy() as data:
        data["description"] = message.text

    await message.answer("Введите сумму в копейках:", reply_markup=reset_kb())
    await IssueInvoice.cost.set()
