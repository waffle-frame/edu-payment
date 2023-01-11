from time import sleep
from os import environ

from models.pushes import Push


async def check_rows_in_sheet(spread_client, shee, db_session, cells: int, file_name: str) -> None:
    """
        check_rows_in_sheet ...
    """
    if cells < 10000:
        return

    file_id = environ.get(f"SPREADSHEETS_{file_name.upper()}")
    test_id = environ.get(f"SPREADSHEETS_TEST")
    new_sheet_number = await Push.update_sheet_num(db_session, file_name)
    
    sheets  = spread_client.open_by_key(test_id)
    example_sheet = sheets.sheet1
    example_sheet.copy_to(file_id)

    print(new_sheet_number, shee._sheet_list)

    sleep(3)        

    shee[new_sheet_number+1].title = f'{new_sheet_number*10000+1}—{(new_sheet_number+1)*10000}'

    return shee[new_sheet_number+1]
