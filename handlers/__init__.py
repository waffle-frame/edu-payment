from aiogram import Dispatcher

from handlers.base import register_base_commands
from handlers.bill import register_payment_commands
from handlers.check_bill import register_check_bill_commands
from handlers.check_manager import register_check_manager_commands

def setup_handlers(dp: Dispatcher):
    register_base_commands(dp)
    register_payment_commands(dp)
    register_check_bill_commands(dp)
    register_check_manager_commands(dp)
