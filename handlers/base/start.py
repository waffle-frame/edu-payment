from aiogram.types import Message

from keyboards.keyboard import operations_kb


# Choose one of the offered operations
async def start(message: Message):
    await message.answer("Приветствую!\nВыберите операцию:", reply_markup=operations_kb())
