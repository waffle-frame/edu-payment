from aiogram import Dispatcher
from pygsheets.client import Client
from sqlalchemy.orm import sessionmaker
from middlewares.dependencies import DependenciesMiddleware


def setup_middlewares(dp: Dispatcher, db_factory: sessionmaker, spread_client: Client):
    dp.middleware.setup(DependenciesMiddleware(db_factory, spread_client))
