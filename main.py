# Packages
from loguru import logger
from aiogram import Dispatcher, executor

# Configs
import handlers
from utils.config import load_config
from utils.bot.update_commands import update_commands
from middlewares import setup_middlewares
from settings.bot import dp
from settings.logger import setup_logger
from settings.database import setup_database

conf = load_config()


# Setup dependencies, handlers, connections
async def start(dp: Dispatcher):
    await update_commands(dp)
    engine, database = setup_database(conf.database)

    setup_middlewares(dp, database)
    setup_logger(conf.logger.path)
    handlers.setup_handlers(dp)

    dp.db_engine = engine   # ???

    logger.info("Bot is successful running!")


# Stop bot and another connections
async def stop(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await dp.db_engine.dispose()
    logger.info("All connections were successfully disconnected!")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup = start, on_shutdown = stop, skip_updates = False)
