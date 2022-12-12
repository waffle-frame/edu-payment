from aiogram import Dispatcher

from handlers.base import register_base_commands

def setup_handlers(dp: Dispatcher):
    register_base_commands(dp)
