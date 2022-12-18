from datetime import datetime

from sqlalchemy_utils.types import ChoiceType
from sqlalchemy import Column, String, DateTime, VARCHAR, BigInteger

from models import Base


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
    created_at = Column(DateTime(timezone=True), default = datetime.utcnow)

    paid_at = Column(DateTime(timezone=True))
    is_paid = Column(ChoiceType(PAYMENT_STATE, impl=String()), default="В ожидании")
    order_id = Column(VARCHAR(50), nullable = False)
    order_link = Column(String, nullable = False)
    creator_data = Column(VARCHAR(100), nullable = False)  # Format: user_id|phone|username

    lesson_type = Column(VARCHAR(20), nullable = False)
    parents_name = Column(VARCHAR(50), nullable = False)
    description = Column(VARCHAR(512))
    amount = Column(BigInteger, nullable = False)
