from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.keyboard import go_back_kb
from keyboards.buttons import go_back
from states.issue_invoice import IssueInvoice


# 
async def description(message: Message, state: FSMContext):
    if message.text == go_back:
        await IssueInvoice.parents_data.set()
        return await message.answer(
            "Введите <b>Фамилию</b> и <b>Имя</b> родителя\n" + \
            "⚠️ Внимание введите данные в указанном порядке:", 
            reply_markup=go_back_kb()
        )

    if len(message.text) > 512:
        return message.answer(
            f"Текст описания не должно превышать 512 символов\nСодержание вашего сообщения:{len(message.text)}"
        )

    async with state.proxy() as data:
        data["description"] = message.text

    await message.answer("Введите сумму в копейках:", reply_markup=go_back_kb())
    await IssueInvoice.cost.set()
