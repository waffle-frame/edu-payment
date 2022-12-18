from google.oauth2.service_account import Credentials
from gspread_asyncio import AsyncioGspreadClientManager, AsyncioGspreadClient

from utils.config import Spreadsheets


def get_creds():
    # sheets.googleapis.com-python.json
    # creds = Credentials.from_service_account_info(
    #     {k: v for k, v in conf.__dict__.items()}
    # )

    creds = Credentials.from_service_account_file("testserviceacct_spreadsheet.json")

    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


async def setup_spread_client(conf: Spreadsheets) -> AsyncioGspreadClient:
    """
        setup_spread_client ...
    """
    
    cre = get_creds

    agcm = AsyncioGspreadClientManager(cre)
    return await agcm.authorize()
