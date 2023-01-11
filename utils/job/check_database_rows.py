from pygsheets.client import Client

from keyboards.buttons import issue_invoice_dict
from utils.spreadsheets.check_new_rows import check_rows
from utils.spreadsheets.create_row import create_rows


async def check_database_rows(db_session, spread_client: Client):
    for file_name in issue_invoice_dict.values():
        data, sheet_num = await check_rows(db_session, file_name)
        if data is None or data == []:
            continue

        print(sheet_num)

        print("PUSH!")
        await create_rows(spread_client, db_session, file_name, data, sheet_num)
