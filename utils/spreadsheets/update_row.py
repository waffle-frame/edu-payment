from os import environ
from typing import List
from loguru import logger
from pygsheets.client import Client
from pygsheets.worksheet import Worksheet

from keyboards.buttons import issue_invoice_prefix
from utils.spreadsheets.check_rows_in_sheet import check_rows_in_sheet


async def update_states(spread_client: Client, db_session, data: List):
    temp_file_name = ""
    for i in data:
        if i[2] != temp_file_name:
            temp_file_name += i[2]
            # file_id = environ.get(f"SPREADSHEETS_TEST")
            file_id = environ.get(f"SPREADSHEETS_{i[2].upper()}")
            sheets = spread_client.open_by_key(file_id)
            sheet: Worksheet = sheets[i[3]]  # type: ignore 

        spread_data = sheet.get_values(start='A2', end='B100000', returnas='matrix')
        prefix = issue_invoice_prefix+i[2]+i[0]
        update_datas = []

        non_empty_rows = []
        for i in spread_data:
            if i != []:
                non_empty_rows.append(i)

        for i in data:
            for j in range(len(spread_data)):
                if prefix == spread_data[j][0]:
                    print("APPEND!!!", i[-1])
                    update_datas.append([i[-1]])

        new_sheet = await check_rows_in_sheet(spread_client, sheets, db_session, len(spread_data), i[2])
        if new_sheet is not None:
            sheet = new_sheet

        try:
            sheet.update_values(crange=f'B2:B{len(spread_data)+1}', values=update_datas)
        except Exception as e:
            logger.error(e)
            pass
