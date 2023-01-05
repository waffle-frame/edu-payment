import json

from typing import Tuple
from loguru import logger 
from aiohttp import ClientSession

from settings.spreadsheets import bill_env

async def generate_bill(description: str, pennies: int, order_number: int) -> Tuple[str, str]:
    """
        generate_bill ...
    """

    # Filling in the request parameters to correctly obtain a link to the payment page
    url = bill_env.get("registerOrderUrl", "")
    params = {
        # Credentials
        "userName": bill_env.get("userName"),
        "password": bill_env.get("password"),
        "expirationDate": bill_env.get("expirationDate"),

        # For building bill
        "description": description,
        "orderNumber": order_number,
        "amount": pennies,
        "returnUrl": bill_env.get("returnUrl"),
    }

    # 
    async with ClientSession() as session:
        while True:
            async with session.get(url, params=params) as bill_request:
                response = await bill_request.read()
                data = json.loads(response)
                logger.info(data)

                if 'errorMessage' in data:
                    if data['errorMessage'] == 'Заказ с таким номером уже обработан':
                        params['orderNumber'] = params['orderNumber'] + 1000
                if "formUrl" in data:
                    await session.close()
                    return data['orderId'], data["formUrl"]
