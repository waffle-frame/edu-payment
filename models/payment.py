from loguru import logger
from typing import Any, List, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy import insert, update, select, desc, between
from sqlalchemy import Column, String, DateTime, VARCHAR, BigInteger


from models import Base
from keyboards.buttons import issue_invoice_prefix


class Payment(Base):
    """
        payment ...
    """
    __tablename__ = "payments"

    PAYMENT_STATE = [
        ("Оплачено", "Оплачено"),
        ("В ожидании", "В ожидании"),
        ("Не aктуально", "Не aктуально"),
    ]

    id = Column(BigInteger, primary_key = True)
    created_at = Column(DateTime(timezone=False), default = datetime.now().replace(microsecond=0))

    paid_at = Column(DateTime(timezone=True))
    status = Column(ChoiceType(PAYMENT_STATE, impl=String()), default="В ожидании")
    order_id = Column(VARCHAR(50))
    order_link = Column(String)
    creator_username = Column(VARCHAR(100))
    creator_telegram_id = Column(BigInteger)

    lesson_type = Column(VARCHAR(20), nullable = False)
    parents_name = Column(VARCHAR(50), nullable = False)
    description = Column(VARCHAR(512))
    amount = Column(BigInteger, nullable = False)

    @classmethod
    async def check_name(cls, session: scoped_session, name: str, **kwargs: Any) -> bool:
        if name.isascii():
            query = select(cls.id).where(cls.creator_username==name).limit(1)
        else:
            query = select(cls.id).where(cls.parents_name==name).limit(1)

        try:
            query_exec = await session.execute(query)
            result = query_exec.fetchone()
            if result is None:
                return False
            return True

        except SQLAlchemyError as e:
            logger.error(f"ROLLBACK EXCEPTION: {e, name, kwargs}")
            return False

    @classmethod
    async def check_invoice(cls, session: scoped_session, order_id: int, lesson_type: str) -> Tuple[str, datetime, str] | None:
        query = select(
            cls.status, cls.created_at, cls.creator_username
        ).where(
            cls.id==order_id, cls.lesson_type==lesson_type
        )

        try:
            query_exec = await session.execute(query)
            result = query_exec.fetchone()
            if result is None:
                return None
            return result

        except SQLAlchemyError as e:
            logger.error(f"ROLLBACK EXCEPTION: {e, order_id}")
            return

    @classmethod
    async def paid_invoice(cls, session: scoped_session, parents_name: str):
        query = select(
            cls.id, cls.lesson_type, cls.amount, cls.created_at
        ).where(
            cls.status=='Оплачено', cls.parents_name==parents_name
        ).order_by(desc(cls.created_at))

        try:
            query_exec = await session.execute(query)
            result = query_exec.fetchall()
            if result is None:
                return None
            data = []

            for i in result:
                data.append([issue_invoice_prefix + i[1] + str(i[0]), i[2], i[3]])
            return data

        except SQLAlchemyError as e:
            logger.error(f"ROLLBACK EXCEPTION: {e}")
            return

    @classmethod
    async def parents_history(cls, session: scoped_session, parents_name: str, period: int):
        start_date = datetime.now() - timedelta(days=period)
        end_date = datetime.now()

        query = select(
            cls.id, cls.lesson_type, cls.amount, cls.description, cls.created_at, cls.creator_username, cls.status
        ).where(
            cls.parents_name==parents_name, between(cls.created_at, start_date, end_date) 
        ).order_by(desc(cls.created_at))

        try:
            query_exec = await session.execute(query)
            result = query_exec.fetchall()
            if result is None:
                return None
            data = []

            for i in result:
                data.append([issue_invoice_prefix + i[1] + str(i[0]), i[2], i[3], i[4], i[5], i[6]])
            return data

        except SQLAlchemyError as e:
            logger.error(f"ROLLBACK EXCEPTION: {e}")
            return

    @classmethod
    async def manager_history(cls, session: scoped_session, from_date: str, to_date: str | None=None, status: str='all', name: str='all'):
        creator_username = cls.creator_username.isnot(None)
        if name != 'all':
            creator_username = cls.creator_username==name

        start_date = datetime.strptime(from_date, '%d-%m-%Y')
        if to_date is not None:
            end_date = datetime.strptime(to_date, '%d-%m-%Y') + timedelta(hours=23, minutes=59, seconds=59)
        else:
            end_date = start_date + timedelta(hours=23, minutes=59, seconds=50)

        query = select(
            cls.id, cls.lesson_type, cls.amount, cls.description, cls.created_at, cls.status, cls.creator_username
        ).where(
            creator_username, cls.created_at.between(start_date, end_date),
            cls.status.in_([i[0] for i in cls.PAYMENT_STATE] if status=='all' else ['Оплачено'])
        ).order_by(desc(cls.created_at))

        try:
            query_exec = await session.execute(query)
            result = query_exec.fetchall()
            if result is None:
                return None
            data = []

            for i in result:
                data.append([issue_invoice_prefix + i[1] + str(i[0]), i[2], i[3], i[4], i[5], i[6]])
            return data

        except SQLAlchemyError as e:
            logger.error(f"ROLLBACK EXCEPTION: {e}")
            return


    @classmethod
    async def create(cls, session: scoped_session, **kwargs: Any):
        query = insert(cls).values(**kwargs).returning(cls.id)

        try:
            result = await session.execute(query)            
            await session.commit()                          # type: ignore
            return result.fetchone()[0]
        except SQLAlchemyError as e:
            logger.error(f"ROLLBACK EXCEPTION: {e, kwargs}")
            return

    @classmethod
    async def update(cls, session: scoped_session, id: int, **kwargs: Any):
        query = update(cls
            ).where(cls.id==id
            ).values(**kwargs
        ).execution_options(synchronize_session="fetch")

        try:
            await session.execute(query)            
            await session.commit()                          # type: ignore
        except SQLAlchemyError as e:
            logger.error(f"ROLLBACK EXCEPTION: {e, kwargs}")
            return

    @classmethod
    async def check_status(cls, session: scoped_session, date_range:int) -> List[Tuple[str, str]]:
        """
            check_status
            :params `date_range` indicated in minutes
        """

        if date_range == 60:
            date_now = datetime.now().date() + timedelta(days=-14)
        elif date_range > 60:
            date_now = datetime.now().date() + timedelta(days=-60)
        else:
            date_now = datetime.now().date()


        date_range_ = date_now + timedelta(days=-date_range)

        query = "SELECT id::varchar, order_id, lesson_type " + \
                "FROM payments " + \
                "WHERE status = 'В ожидании' " + \
                f"AND created_at BETWEEN '{date_range_.__str__() + (' 00:00:00')}'::timestamp and '{date_now.__str__() + (' 23:59:59')}'::timestamp " + \
                "ORDER BY lesson_type;"
    
        try:
            query_exec = await session.execute(query)
            result = query_exec.fetchall()
            return [ tuple(i) for i in result]
        except SQLAlchemyError as e:
            logger.error(f"ROLLBACK: {e, date_range}")
            await session.rollback()                        # type: ignore
            return                                          # type: ignore
