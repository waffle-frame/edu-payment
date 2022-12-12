import os, sys
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__))+os.sep+os.pardir)

from utils.config import load_config
from settings.database import setup_database


async def create_table():
    conf = load_config().database
    engine, _= setup_database(conf)
    async with engine.begin() as conn:
        await conn.run_sync()

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_table())
