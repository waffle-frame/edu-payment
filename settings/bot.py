# Packages
from aiogram import Bot, Dispatcher
from aiogram.types.message import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Configs
from utils.config import load_config

conf = load_config()

bot = Bot(
    token = conf.bot.token,
    parse_mode = ParseMode.HTML,
    validate_token = True
)

dp = Dispatcher(bot, storage=MemoryStorage())
