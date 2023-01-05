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

async def check_bill(order_data: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
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
    # 
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

                    if "orderStatus" in data:
                        # logger.info(data)
                        print(order_data[index], type(order_data[index]))
                        order_data[index] += error_code_to_string[data["orderStatus"]],
                        if data["orderStatus"] == 2:
                            order_data.remove(order_data[index])
                            break
                        break
        await session.close()
    return order_data
