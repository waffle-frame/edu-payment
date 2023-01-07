from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher.filters.builtin import Command

from handlers.check_bill.start_check_bill import start_check_bill
from handlers.check_bill.parents_name_or_invoice_data import parents_name_or_invoice_data
from handlers.check_bill.parents_history_operations import parents_history_operations
from handlers.check_bill.callbacks import parents_history_days_cb 

from states.check_bill import CheckBill
from keyboards.buttons import operations_list


def register_check_bill_commands(dp: Dispatcher):
    dp.register_message_handler(start_check_bill, Text(equals=[operations_list[1], '/check_invoice']), state="*")

    dp.register_message_handler(parents_name_or_invoice_data, state=CheckBill.parameter)
    dp.register_message_handler(parents_history_operations, state=CheckBill.parents_history_operations)

    # Callbacks
    dp.register_callback_query_handler(parents_history_days_cb, lambda call: call.data.startswith('phistory_'), state='*')
