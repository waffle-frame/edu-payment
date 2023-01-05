from pygsheets.client import Client

from models.payment import Payment
from utils.bill.check_status import check_bill
from utils.spreadsheets.update_row import update_states


async def check_bill_last_14_days_job(db_session,  spread_client: Client):
    order_ids = await Payment.check_status(db_session, 999)

    orders = await check_bill(order_ids)

    update_states(spread_client, orders)




async def check_bill_last_60_days_job(db_session,  spread_client: Client):
    await Payment.check_status(db_session, 60)


async def check_bill_over_60_days_job(db_session,  spread_client: Client):
    await Payment.check_status(db_session, 60*100)
