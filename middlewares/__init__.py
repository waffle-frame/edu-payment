from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker
from gspread_asyncio import AsyncioGspreadClient
from middlewares.dependencies import DependenciesMiddleware


def setup_middlewares(dp: Dispatcher, db_factory: sessionmaker, spread_client: AsyncioGspreadClient):
    dp.middleware.setup(DependenciesMiddleware(db_factory, spread_client))
