operations_list = ["Выставить счет", "Проверить платёж", "Проверить менеджера"]
issue_invoice_dict = {
    "Групповые👥": "group", "Индивидуальные👤": "individual",
    "Интенсив👨‍🏫": "intensive", "Короткий проект📄": "short",
    "Спецкурс": "special"
}

issue_invoice_prefix = 'tg2_'
validation_list = ['✅', '❌']
manager_history_operations_list = ['По менеджеру', 'По дате, диапазону']
manager_history_date_range_operations_dict = {"По дате создания": 'created_at', "По дате оплаты": "paid_at"}
parent_history_operations_list = ['Оплаченные платежи', 'Созданные на родителя платежи']
