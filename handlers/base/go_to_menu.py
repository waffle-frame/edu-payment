from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.keyboard import operations_kb


# Choose one of the offered operations
async def go_to_menu(message: Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.finish()

    await message.answer("Выберите операцию:", reply_markup=operations_kb())
