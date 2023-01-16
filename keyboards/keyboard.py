from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from utils.bot.list_to_buttons import list_to_buttons
from keyboards.buttons import operations_list, issue_invoice_dict, \
    validation_list, parent_history_operations_list, manager_history_operations_list, \
    manager_history_date_range_operations_dict, go_back


def operations_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons(operations_list),
        resize_keyboard=True, one_time_keyboard=True
    )

def parents_history_operations_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons(parent_history_operations_list),
        resize_keyboard=True, one_time_keyboard=True
    )

def manager_history_operations_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons(manager_history_operations_list),
        resize_keyboard=True, one_time_keyboard=True
    )

def manager_history_date_range_operations_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons(list(manager_history_date_range_operations_dict.keys())),
        resize_keyboard=True, one_time_keyboard=True
    )

def filter_by_manager_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons(list("Я")),
        resize_keyboard=True, one_time_keyboard=True
    )

def issue_invoice_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons(list(issue_invoice_dict.keys())),
        resize_keyboard=True, one_time_keyboard=True
    )

def reset_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()

def go_back_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons([go_back]),
        resize_keyboard=True, one_time_keyboard=True
    )

def validation_kb() -> ReplyKeyboardMarkup:
    data = validation_list.copy()
    data.append(go_back)
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons(data),
        one_time_keyboard=True
    )


def parents_history_cbkb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        resize_keyboard=False, 
        inline_keyboard=[
            [
                InlineKeyboardButton('7 дней', callback_data='phistory_7days'),
                InlineKeyboardButton('30 дней', callback_data='phistory_30days'),
                InlineKeyboardButton('За все время', callback_data='phistory_99999days'),
            ]
        ]
    )

def manager_history_cbkb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        resize_keyboard=False,
        inline_keyboard=[
            [
                InlineKeyboardButton('Все', callback_data='mhistory_all'),
                InlineKeyboardButton('Оплаченные', callback_data='mhistory_paid'),
            ]
        ]
    )

def manager_history_periods_cbkb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        resize_keyboard=False,
        inline_keyboard=[
            [
                InlineKeyboardButton('Последние 7 дней', callback_data='mperiod_history_7days'),
                InlineKeyboardButton('Последние 30 дней', callback_data='mperiod_history_30days'),
            ],
            [
                InlineKeyboardButton('Весь период', callback_data='mperiod_history_9999days'),
            ]
        ]
    )