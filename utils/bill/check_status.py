import json

from loguru import logger 
from typing import List, Tuple
from aiohttp import ClientSession

from settings.spreadsheets import bill_env

error_code_to_string = {
    0: "В ожидании",
    2: "Оплачено",
    6: "Не актуально",
}

async def check_bill(order_data: List) -> List:
    """
        check_bill ...
    """

    # TODO: EXPLAIN

    url = bill_env.get("checkOrderUrl", "")
    params = {
        # Credentials
        "userName": bill_env.get("userName"),
        "password": bill_env.get("password"),
    }

    updated_order_data = []

    async with ClientSession() as session:
        for index in range(len(order_data)):
            if order_data[index][1] is None:
                logger.error(f"order id is not found, ID: {order_data[index]}")
                continue

            params["orderId"] = order_data[index][1]
            while True:
                async with session.get(url, params=params) as bill_request:
                    response = await bill_request.read()
                    data = json.loads(response)

                    if "errorCode" in data:
                        if data["errorCode"] == '6':
                            logger.error(f"response is {data['errorMessage']}, Data: {order_data[index]}")
                            break

                    # Set
                    if "orderStatus" in data:
                        if data["orderStatus"] != 0:
                            order_data[index].append(error_code_to_string[data["orderStatus"]])
                            updated_order_data.append(order_data[index])
                        break

        await session.close()
    return updated_order_data
