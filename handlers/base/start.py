from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.keyboard import operations_kb, parents_history_cbkb


# Choose one of the offered operations
async def start(message: Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.finish()

    await message.answer("Приветствую!\nВыберите операцию:", reply_markup=operations_kb())
