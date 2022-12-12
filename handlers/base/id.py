from aiogram.types import Message

async def get_id(message: Message):
    await message.answer(message.chat.id)
