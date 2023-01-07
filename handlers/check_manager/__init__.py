from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import Text

from handlers.check_manager.start_check_manager import start_check_manager
from handlers.check_manager.username import username
from handlers.check_manager.date import date

from handlers.check_manager.callback import manager_history_period_cb

from states.check_manager import CheckManager
from keyboards.buttons import operations_list


def register_check_manager_commands(dp: Dispatcher):
    dp.register_message_handler(start_check_manager, Text(equals=[operations_list[2], '/check_manager']), state="*")

    dp.register_message_handler(username, state=CheckManager.username)
    dp.register_message_handler(date, state=CheckManager.date)

    # Callbacks
    dp.register_callback_query_handler(manager_history_period_cb, lambda call: call.data.startswith('mhistory_'), state='*')
