from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from middlewares.dependencies import DependenciesMiddleware


def setup_middlewares(dp: Dispatcher, db_factory: sessionmaker):
    dp.middleware.setup(DependenciesMiddleware(db_factory))
