from os import environ
from pygsheets.client import Client
from pygsheets.worksheet import Worksheet


def create_rows(spread_client: Client, file: str, data):
    """
        create_rows ...
    """

    file_id = environ.get(f"SPREADSHEETS_{file.upper()}")
    spreads = spread_client.open_by_key(file_id)
    spread: Worksheet = spreads[0]

    cells = spread.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False)

    non_empty_rows = []
    for i in cells:
        if i != []:
            non_empty_rows.append(i)

    spread.insert_rows(len(non_empty_rows), values=data, inherit=False)

    