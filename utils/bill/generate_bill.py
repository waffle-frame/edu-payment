import json

from os import environ
from loguru import logger 
from random import randint
from aiohttp import ClientSession


async def generate_bill(description: str, pennies: int) -> str:
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
        "orderNumber": randint(1, 256*10),
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
                    return data["formUrl"]
