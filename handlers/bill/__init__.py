from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import Text

from handlers.bill.start_issue_invoice_operation import start_issue_invoice_operation
from handlers.bill.lesson_type import lesson_type
from handlers.bill.parents_data import parents_data
from handlers.bill.description import description
from handlers.bill.cost import cost
from handlers.bill.validation import validation

from states.issue_invoice import IssueInvoice
from keyboards.keyboard import operations_list


def register_payment_commands(dp: Dispatcher):
    dp.register_message_handler(start_issue_invoice_operation, Text(equals=[operations_list[0]]))

    dp.register_message_handler(lesson_type, state=IssueInvoice.lesson_type)
    dp.register_message_handler(parents_data, state=IssueInvoice.parents_data)
    dp.register_message_handler(description, state=IssueInvoice.description)
    dp.register_message_handler(cost, state=IssueInvoice.cost)
    dp.register_message_handler(validation, state=IssueInvoice.validation)