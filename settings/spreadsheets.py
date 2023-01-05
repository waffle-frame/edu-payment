from pygsheets import authorize
from pygsheets.client import Client

from utils.config import Spreadsheets, Bill

bill_env: dict = {}

def setup_spread_client(spread: Spreadsheets, bill: Bill) -> Client:
    """
        setup_spread_client ...
    """

    global bill_env
    bill_env["asd"] = "asdasd"
    bill_env["userName"] = bill.username
    bill_env["password"] = bill.password
    bill_env["expirationDate"] = bill.expiration_date
    bill_env["returnUrl"] = bill.redirect_url
    bill_env["checkOrderUrl"] = bill.check_order_url
    bill_env["registerOrderUrl"] = bill.register_order_url

    return authorize(outh_file=spread.account_file)
