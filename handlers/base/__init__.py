from typing import Any
from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher.filters.builtin import Command, CommandHelp, CommandStart

import handlers.base.cancel as _
from handlers.base.help import help
from handlers.base.id import get_id
from handlers.base.start import start
from handlers.base.go_to import go_to_menu


def register_base_commands(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart(), state='*')
    dp.register_message_handler(help, CommandHelp(), state="*")
    dp.register_message_handler(get_id, Command("id"), state="*")
    dp.register_message_handler(go_to_menu, Text(equals=['◀️ В главное меню']), state='*')
