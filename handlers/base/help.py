from aiogram.types import Message

async def help(message: Message):
    help_message = "Помощь:\n" + \
        "/start — Запустить бота\n" + \
        "/help — Вывести это сообщение\n" + \
        "/invoice — Выставить счет" + \
        "/check_invoice — Проверить платеж" + \
        "/check_by_filter — Проверить по фильтру"

    await message.answer(help_message)
