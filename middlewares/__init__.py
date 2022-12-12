from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from middlewares.dependencies import SQLAlchemyMiddleware


def setup_middlewares(dp: Dispatcher, db_factory: sessionmaker):
    dp.middleware.setup(SQLAlchemyMiddleware(db_factory))
