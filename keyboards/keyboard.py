from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from utils.bot.list_to_buttons import list_to_buttons

operations_list = ["Выставить счет", "Проверить платёж"]
issue_invoice_dict = {
    "Групповые👥": "group", "Индивидуальные👤": "individual",
    "Интенсив👨‍🏫": "intensive", "Короткий проект📄": "short",
    "Спецкурс": "special", 
}

issue_invoice_prefix = 'tg2_'
validation_list = ['✅', '❌']


def operations_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons(operations_list),
        resize_keyboard=True, one_time_keyboard=True
    )

def issue_invoice_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons(issue_invoice_dict.keys()),
        resize_keyboard=True, one_time_keyboard=True
    )

def reset_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()

def validation_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=list_to_buttons(validation_list),
        one_time_keyboard=True
    )
