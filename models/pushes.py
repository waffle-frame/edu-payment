from typing import Any
from loguru import logger

from sqlalchemy import select, update
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, VARCHAR, BigInteger

from models import Base
from keyboards.buttons import issue_invoice_prefix


class Push(Base):
    """
        push ...
    """
    __tablename__ = "pushes"


    id = Column(BigInteger, primary_key = True)
    file = Column(VARCHAR, nullable = False)
    offset = Column(BigInteger, default=1)
    limit = Column(BigInteger, default=50)

    @classmethod
    async def select(cls, session: scoped_session, **kwargs: Any):
        try:
            query = select(cls)
            result = await session.execute(query)            
            await session.commit()                          # type: ignore
            return result
        except SQLAlchemyError as e:
            logger.error("ROLLBACK:", e, kwargs)
            await session.rollback()                        # type: ignore
            return

    @classmethod
    async def update_offset(cls, session: scoped_session, file: str, offset: int):
        query = update(cls).where(cls.file==file).values(offset=offset)
        await session.execute(query)
        await session.commit()                              # type: ignore
        return

    @classmethod
    async def get_data_for_upload(cls, session: scoped_session, offset: int):
        # TODO: EXPLAIN
        query = f"""SELECT ('{issue_invoice_prefix}' || lesson_type || id), ('=INT(' || amount || '/100)&","&MOD(' || amount || ';100)&" ₽"'), status, """ + \
                    """('=HYPERLINK("' || order_link || '";"' || order_id ||  '")'),""" + \
                    "description, parents_name, '@' || split_part(creator_data, '|', 2)," + \
                    "COALESCE(to_char(created_at, 'mm/dd/yyyy HH24:MI:SS'), '')\n" + \
                f"FROM payments OFFSET {offset};"

        data_exec = await session.execute(query)
        return [ list(i) for i in data_exec.fetchall()]
