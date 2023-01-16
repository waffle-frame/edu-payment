# Packages
from loguru import logger
from aiogram import Dispatcher, executor

# Configs
import handlers
from utils.config import load_config
from utils.bot.update_commands import update_commands
from middlewares import setup_middlewares

# Settings
from settings.bot import dp
from settings.logger import setup_logger
from settings.database import setup_database
from settings.scheduler import setup_scheduler
from settings.spreadsheets import setup_spread_client


# Setup dependencies, handlers, connections
async def start(dp: Dispatcher):
    conf = load_config()

    spread_client = setup_spread_client(conf.spreadsheets, conf.bill)
    engine, database  = setup_database(conf.database)
    setup_middlewares(dp, database, spread_client)
    await setup_scheduler(database, spread_client)

    await update_commands(dp)
    setup_logger(conf.logger.path)
    handlers.setup_handlers(dp)

    # ???
    dp['db_engine'] = engine
    dp['spread_client'] = spread_client

    logger.info("Bot is successful running!")


# Stop bot and another connections
async def stop(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    # await dp['db_engine'].dispose()
    logger.info("All connections were successfully disconnected!")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup = start, on_shutdown = stop, skip_updates = False)
