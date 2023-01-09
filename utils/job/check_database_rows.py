from pygsheets.client import Client

from keyboards.buttons import issue_invoice_dict
from utils.spreadsheets.check_rows import check_rows
from utils.spreadsheets.create_row import create_rows


async def check_database_rows(db_session, spread_client: Client):
    for file_name in issue_invoice_dict.values():
        data = await check_rows(db_session, file_name)
        if data is None or data == []:
            continue

        print("PUSH!")
        create_rows(spread_client, file_name, data)
