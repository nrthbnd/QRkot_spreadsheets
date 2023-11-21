from sqlalchemy import Column, ForeignKey, Integer, Text

from constants import (
    USER_ID_FK_MD,
    USER_ID_FK_NAME,
)
from app.models.custombase import CustomBase


class Donation(CustomBase):
    """Модель пожертвований."""
    user_id = Column(
        Integer,
        ForeignKey(USER_ID_FK_MD, name=USER_ID_FK_NAME)
    )
    comment = Column(Text)
