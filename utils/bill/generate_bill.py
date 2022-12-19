import json

from os import environ
from typing import Tuple
from loguru import logger 
from aiohttp import ClientSession


async def generate_bill(description: str, pennies: int, order_number: int) -> Tuple[str, str]:
                    #  parent_name, who_issued_the_payment, payments_purposes_table_id, payments_tables):
    """
        generate_bill ...
    """

    # Filling in the request parameters to correctly obtain a link to the payment page.
    url = environ.get("BILL_URL", "")
    params = {
        # Credentials
        "userName": environ.get("BILL_USERNAME"),
        "password": environ.get("BILL_PASSWORD"),
        "expirationDate": environ.get("BILL_EXPIRATION_DATE"),

        # For building bill
        "description": description,
        "orderNumber": order_number,
        "amount": pennies,
        "returnUrl": environ.get("BILL_REDIRECT_URL"),
    }

    # 
    async with ClientSession() as session:
        while True:
            async with session.get(url, params=params) as bill_request:
                response = await bill_request.read()
                data = json.loads(response)
                logger.info(data)

                if "formUrl" in data:
                    await session.close()
                    return data['orderId'], data["formUrl"]
