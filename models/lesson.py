from models import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(BigInteger, primary_key = True)

    lesson = relationship("Lesson", back_populates="teacher")
    name = Column(String(32))
    surname = Column(String(32))
