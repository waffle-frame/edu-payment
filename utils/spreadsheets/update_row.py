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
            file_id = environ.get(f"SPREADSHEETS_{i[2].upper()}")
            sheets = spread_client.open_by_key(file_id)
            sheet: Worksheet = sheets[i[3]]  # type: ignore 

        spread_data = sheet.get_values(start='A2', end='B100000')
        prefix = issue_invoice_prefix+i[2]+i[0]
        cells = []

        print(spread_data, data)

        for i in data:
            for j in range(len(spread_data)):
                print(prefix, spread_data[j][0])
                if prefix == spread_data[j][0]:
                    cells.append([prefix, i[3]])

        spread = await check_rows_in_sheet(spread_client, sheets, db_session, len(spread_data), i[2])

        try:
            spread.update_values(crange='A2:B100000', values=cells)
        except Exception as e:
            logger.error(e)
