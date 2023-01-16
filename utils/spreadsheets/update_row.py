from os import environ
from typing import List
from pygsheets.client import Client
from pygsheets.worksheet import Worksheet

from settings.bot import bot
from keyboards.buttons import issue_invoice_prefix


async def update_states(spread_client: Client, data: List):
    temp_file_name = ""
    crange, update_data = [], []

    message_text = 'Поступило уведомление о состоянии вашей платежки:\n\n' + \
        'Номер заказа: <code>{order}</code>\n' + \
        'Статус: {status}\n' + \
        'Время: {time}\n'

    sheet = ""
    for i in data:
        if i[1] != temp_file_name:
            if temp_file_name != "":
                sheet.update_values_batch(crange, update_data)

            temp_file_name = i[1]
            crange, update_data = [], []

            file_id = environ.get(f"SPREADSHEETS_{i[1].upper()}")
            sheets = spread_client.open_by_key(file_id)
            sheet: Worksheet = sheets[i[2]]  # type: ignore 

        crange.append(f'B{i[3]}')
        crange.append(f'I{i[3]}')
        update_data.append([[i[5]]])
        update_data.append([[i[-1].strftime('%d/%m/%Y %H:%m')]])

        await bot.send_message(i[4], message_text.format(
                order=issue_invoice_prefix + i[1] + str(i[3]), 
                status=i[5],
                time=i[-1].strftime('%d/%m/%Y %H:%m')
            )
        )

    if crange != []:
        sheet.update_values_batch(crange, update_data)
