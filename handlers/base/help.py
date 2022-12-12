from aiogram.types import Message

async def help(message: Message):
    help_message = "Помощь:\n" + \
        "/start — Запустить бота\n" + \
        "/help — Вывести это сообщение\n"

    await message.answer(help_message)
