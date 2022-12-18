from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from gspread_asyncio import AsyncioGspreadClient
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DependenciesMiddleware(LifetimeControllerMiddleware):
    def __init__(self, db_factory: sessionmaker, spread_client: AsyncioGspreadClient):
        self.db_factory = db_factory
        self.spread_client = spread_client
        super().__init__()

    async def pre_process(self, obj, data, *args):
        db: Session = self.db_factory()
        spread_client: AsyncioGspreadClient = self.spread_client
        data["spread_client"] = spread_client
        data["db"] = db

    async def post_process(self, obj, data, *args):
        db: AsyncSession = data.get("db")
        await db.close()
