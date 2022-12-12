from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from utils.config import Database


# Setup async connection SQLAlchemy with postgres database
def setup_database(conf: Database):
    url = f"postgresql+asyncpg://{conf.username}:{conf.password}@{conf.host}:{conf.port}/{conf.db_name}"

    engine = create_async_engine(
        url,
        query_cache_size = 1200,
        pool_size = 100,
        max_overflow = 200,
        future = True,
        echo = False,
    )

    return engine, sessionmaker(
        bind = engine, expire_on_commit = False, class_ = AsyncSession
    )
