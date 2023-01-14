from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from states.check_manager import CheckManager
from keyboards.buttons import manager_history_date_range_operations_dict
from keyboards.keyboard import manager_history_date_range_operations_kb, reset_kb

#
async def date_range(message: Message, state: FSMContext):
    param = manager_history_date_range_operations_dict.get(message.text, None)
    if param is None:
        return await message.answer(
            "Неизвестная комбинация. Повторите попытку", 
            reply_markup=manager_history_date_range_operations_kb(),
        )

    async with state.proxy() as data:
        data["date_range_param"] = manager_history_date_range_operations_dict[message.text]

    await CheckManager.date.set()

    await message.answer(
        "Дату или диапазон\n\n" +\
        "Пример даты: 01.01.2023\n" +\
        "Пример диапазона: 01.01.2023 10.01.2023",
        reply_markup=reset_kb()
    )
