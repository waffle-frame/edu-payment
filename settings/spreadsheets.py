from google.auth.credentials import Scoped
from google.oauth2.service_account import Credentials
from gspread_asyncio import AsyncioGspreadClientManager, AsyncioGspreadClient

from utils.config import Spreadsheets


def get_creds() -> Scoped:
    """
        get_creds ...
    """
    creds = Credentials.from_service_account_file(data)

    return creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])



async def setup_spread_client(conf: Spreadsheets) -> AsyncioGspreadClient:
    """
        setup_spread_client ...
    """
    global data
    data = conf.account_file

    agcm = AsyncioGspreadClientManager(get_creds)
    return await agcm.authorize()
