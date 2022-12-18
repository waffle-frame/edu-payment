from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DependenciesMiddleware(LifetimeControllerMiddleware):
    def __init__(self, db_factory: sessionmaker):
        self.db_factory = db_factory
        # self.spread = spread_cliend
        super().__init__()

    async def pre_process(self, obj, data, *args):
        db: Session = self.db_factory()
        # spread_client: AsyncioGspreadClient = self.spread.get_client()
        data["db"] = db

    async def post_process(self, obj, data, *args):
        db: AsyncSession = data.get("db")
        await db.close()
