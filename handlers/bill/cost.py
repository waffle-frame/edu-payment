from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.keyboard import validation_kb
from states.issue_invoice import IssueInvoice


# 
async def cost(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Не верный тип данных. Введите стоимость в цифрах\n\nНапример: 300000")

    async with state.proxy() as data:
        data["cost"] = message.text

    data = await state.get_data()
    data.get("asd")
    await IssueInvoice.validation.set()
    await message.answer( text=f"Все верно?\n"
        f"<b>Тип Занятий</b>: {data.get('lesson_type')}\n"
        f"<b>Имя родителя</b>: {data.get('parent_data')}\n"
        f"<b>Описание</b>: {data.get('description')}\n"
        f"<b>Стоимость</b>: {str(int(data.get('cost', 0)) // 100)} руб. {str(int(data.get('cost', 0)) % 100)} коп.", 
        reply_markup=validation_kb()
    )
