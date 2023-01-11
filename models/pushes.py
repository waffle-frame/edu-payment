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
    offset = Column(BigInteger, default=0)
    sheet = Column(BigInteger, default=1)

    @classmethod
    async def get_offset(cls, session: scoped_session, file_name: str) -> int:
        query = select(cls.offset).where(cls.file == file_name)

        try:
            query_exec = await session.execute(query)
            result = query_exec.fetchone()
            if result is not None:
                return result[0]
            return 0
        except SQLAlchemyError as e:
            logger.error("ROLLBACK: ", file_name, e)
            return 0

    @classmethod
    async def update_offset(cls, session: scoped_session, file: str, offset: int):
        query = update(cls).where(cls.file==file).values(offset=offset+1)
        await session.execute(query)
        await session.commit()                              # type: ignore
        return

    @classmethod
    async def update_sheet_num(cls, session: scoped_session, file: str):
        query = f"UPDATE pushes SET sheet=sheet+1 WHERE file = '{file}' RETURNING sheet"

        query_exec = await session.execute(query)
        await session.commit()                              # type: ignore
        return query_exec.fetchone()[0]

    @classmethod
    async def get_data_for_upload(cls, session: scoped_session, offset: int, file_name: str):
        # TODO: EXPLAIN
        query_data = f"""
            SELECT ('{issue_invoice_prefix}' || lesson_type || id), 
                    status,
                    ('=INT(' || amount || '/100)&","&MOD(' || amount || ';100)&" ₽"'), 
                    ('=HYPERLINK("' || order_link || '";"' || order_id ||  '")'),
                    description, parents_name, '@' || creator_username,
                    COALESCE(to_char(created_at, 'mm/dd/yyyy HH24:MI:SS'), '')
            FROM payments WHERE lesson_type='{file_name}' OFFSET {offset};
        """

        query_sheet_num = select(cls.sheet).where(cls.file == file_name)

        try:
            exec_sheet_num = await session.execute(query_sheet_num)
            sheet_num = exec_sheet_num.fetchone()[0]

            data_exec = await session.execute(query_data)
            result = data_exec.fetchall()
            if result == []:
                return None, sheet_num

            query_update = f"""UPDATE  pushes SET "offset"="offset"+{len(result)} WHERE file='{file_name}'"""
            await session.execute(query_update)
            await session.commit()                          # type: ignore

            return [ list(i) for i in result ], sheet_num

        except SQLAlchemyError as e:
            logger.error(f"ROLLBACK: {e}")
            await session.rollback()                        # type: ignore
            return None, sheet_num                          # type: ignore
