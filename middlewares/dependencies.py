from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class SQLAlchemyMiddleware(LifetimeControllerMiddleware):
    def __init__(self, db_factory: sessionmaker):
        self.db_factory = db_factory
        super().__init__()

    async def pre_process(self, obj, data, *args):
        db: AsyncSession = self.db_factory()
        data["db"] = db

    async def post_process(self, obj, data, *args):
        db: AsyncSession = data.get("db")
        await db.close()
