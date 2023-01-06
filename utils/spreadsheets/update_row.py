from os import environ
from loguru import logger
from typing import List, Tuple
from pygsheets.client import Client
from pygsheets.custom_types import HorizontalAlignment
from pygsheets.worksheet import Worksheet, Cell, Address

from utils.spreadsheets.colors import colors
from keyboards.buttons import issue_invoice_prefix


def update_states(spread_client: Client, data: List[Tuple[str, str, str, str]]):
    file_id = environ.get(f"SPREADSHEETS_TEST")
    spreads = spread_client.open_by_key(file_id)
    spread: Worksheet = spreads[0]  # type: ignore

    spread_data = spread.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)
    cells = []

    for i in data:
        for j in range(len(spread_data)):
            if issue_invoice_prefix+i[2]+i[0] == spread_data[j][0]:
                cell = Cell(Address(f"C{j+1}"), val=i[3])
                cell.color = colors[i[3]]
                cell.set_horizontal_alignment(HorizontalAlignment.CENTER)
                cells.append(cell)

    try:
        spread.update_cells(cells)
    except Exception as e:
        logger.error(e)
