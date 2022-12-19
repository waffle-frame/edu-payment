from pygsheets import authorize
from pygsheets.client import Client

from utils.config import Spreadsheets


def setup_spread_client(conf: Spreadsheets) -> Client:
    """
        setup_spread_client ...
    """

    return authorize(outh_file=conf.account_file)
