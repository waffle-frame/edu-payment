from aiogram import Dispatcher

from handlers.base import register_base_commands
from handlers.bill import register_payment_commands
from handlers.check_bill import register_check_commands


def setup_handlers(dp: Dispatcher):
    register_base_commands(dp)
    register_payment_commands(dp)
    register_check_commands(dp)
