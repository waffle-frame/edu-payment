from os import environ

from pygsheets.client import Client
from pygsheets.worksheet import Worksheet

from utils.spreadsheets.check_rows_in_sheet import check_rows_in_sheet


async def create_rows(spread_client: Client, db_session,  file: str, data, sheet_num: int):
    """
        create_rows ...
    """

    file_id = environ.get(f"SPREADSHEETS_{file.upper()}")
    sheets  = spread_client.open_by_key(file_id)
    sheet: Worksheet = sheets[sheet_num]

    cells = sheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False)    

    non_empty_rows = []
    for i in cells:
        if i != []:
            non_empty_rows.append(i)

    new_sheet = await check_rows_in_sheet(spread_client, sheets, db_session, len(non_empty_rows), file)
    if new_sheet is not None:
        sheet = new_sheet 

    sheet.insert_rows(len(non_empty_rows), values=data, inherit=False)
