from pygsheets.client import Client
from sqlalchemy.orm import scoped_session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.job.check_database_rows import check_database_rows
from utils.job.check_bill import check_bill_last_14_days_job, \
    check_bill_last_60_days_job, check_bill_over_60_days_job, \
    check_bill_last_3_days_job, check_bill_last_7_days_job


async def setup_scheduler(db_session: scoped_session, spread_client: Client):
    scheduler = AsyncIOScheduler(job_defaults={'max_instances': 5})

    scheduler.add_job(check_bill_last_3_days_job, trigger='interval', seconds=15, kwargs={"db_session": db_session(), "spread_client": spread_client})
    scheduler.add_job(check_bill_last_7_days_job, trigger='interval', minutes=5, kwargs={"db_session": db_session(), "spread_client": spread_client})
    scheduler.add_job(check_bill_last_14_days_job, trigger='interval', minutes=10, kwargs={"db_session": db_session(), "spread_client": spread_client})
    scheduler.add_job(check_bill_last_60_days_job, trigger='interval', hours=1, kwargs={"db_session": db_session(), "spread_client": spread_client})
    scheduler.add_job(check_bill_over_60_days_job, trigger='interval', days=1, kwargs={"db_session": db_session(), "spread_client": spread_client})

    scheduler.add_job(check_database_rows, trigger='interval', seconds=10, kwargs={"db_session": db_session(), "spread_client": spread_client})

    scheduler.start()
