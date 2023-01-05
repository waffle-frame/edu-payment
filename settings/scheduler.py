from pygsheets.client import Client
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.job.check_bill import check_bill_last_14_days_job


async def setup_scheduler(db_session: AsyncSession, spread_client: Client):
    scheduler = AsyncIOScheduler(job_defaults={'max_instances': 2})

    # await check_bill_last_14_days_job(db_session(), spread_client)
    scheduler.add_job(check_bill_last_14_days_job, 'interval', seconds=15, kwargs={"db_session": db_session(), "spread_client": spread_client})

    scheduler.start()
