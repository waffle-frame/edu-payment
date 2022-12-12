import sys
from loguru import logger

def setup_logger(LOGGER_PATH: str):
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    logger.add(LOGGER_PATH + "/log.log")
