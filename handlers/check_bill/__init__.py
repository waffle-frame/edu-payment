from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import Text

from handlers.check_bill.start_check_bill import start_check_bill
from handlers.check_bill.parents_name_or_invoice_data import parents_name_or_invoice_data
from handlers.check_bill.parents_history_operations import parents_history_operations

from states.check_bill import CheckBill
from keyboards.buttons import operations_list


def register_check_commands(dp: Dispatcher):
    dp.register_message_handler(start_check_bill, Text(equals=[operations_list[1]]))

    dp.register_message_handler(parents_name_or_invoice_data, state=CheckBill.parameter)
    dp.register_message_handler(parents_history_operations, state=CheckBill.parents_history_operations)
