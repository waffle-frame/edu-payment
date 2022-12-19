from loguru import logger
from pygsheets.client import Client


def create_row(client: Client, file_id: str | None):
    """
        create_row
    """

    if file_id is None:
        logger.error("value of field_id is none")
        return

    spread = client.open_by_key(file_id)
    print('SPREADSHEETS_' + sdata["lesson_type"].split("_")[1].upper())
    file_id = environ.get('SPREADSHEETS_' + sdata["lesson_type"].split("_")[1].upper())
    payment_str = 'Номер заказа: ' + payment_info[0] + '\nСсылка на оплату:\n' + payment_info[1]['formUrl']