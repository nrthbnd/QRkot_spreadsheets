from sqlalchemy import Boolean, Column, DateTime, Integer

from constants import (
    INVESTED_AMOUNT_DEFAULT,
    FULLY_INVESTED_DEFAULT,
    CREATE_DATE_DEFAULT,
    CLOSE_DATE_DEFAULT,
)
from app.core.db import Base


class CustomBase(Base):
    """Абстрактный базовый класс для моделей CharityProject и Donation."""
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=INVESTED_AMOUNT_DEFAULT)
    fully_invested = Column(Boolean, default=FULLY_INVESTED_DEFAULT)
    create_date = Column(DateTime, default=CREATE_DATE_DEFAULT)
    close_date = Column(DateTime, default=CLOSE_DATE_DEFAULT)
