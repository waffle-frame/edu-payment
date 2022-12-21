import os, sys
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__))+os.sep+os.pardir)

from sqlalchemy import insert
from models.pushes import Push
from utils.config import load_config
from settings.database import setup_database

async def insert_data():
    conf = load_config().database
    engine, _= setup_database(conf)
    
    data = ["test","group","short","special","intensive","individual"]

    async with engine.begin() as conn:
        for i in data:
            await conn.execute(insert(Push).values(file=i))
        await conn.commit()

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(insert_data())
