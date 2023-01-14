from os import environ
from typing import List
from pygsheets.client import Client
from pygsheets.worksheet import Worksheet



async def update_states(spread_client: Client, data: List):
    temp_file_name = ""
    for i in data:
        if i[1] != temp_file_name:
            temp_file_name = i[1]
            file_id = environ.get(f"SPREADSHEETS_{i[1].upper()}")
            sheets = spread_client.open_by_key(file_id)
            sheet: Worksheet = sheets[i[2]]  # type: ignore 

        crange, update_data = [], []
        for i in data:
            crange.append(f'B{i[3]}')
            crange.append(f'I{i[3]}')
            update_data.append([[i[4]]])
            update_data.append([[i[-1].strftime('%d/%m/%Y %H:%m')]])

        print(crange, update_data)

        sheet.update_values_batch(crange, update_data)
