from aiogram.types import BotCommand
from aiogram.dispatcher import Dispatcher

async def update_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        BotCommand("help", "Помощь"),
        BotCommand("start", "Запустить бота"),
    ])
