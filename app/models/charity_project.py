from sqlalchemy import Column, String, Text

from constants import PR_NAME_MAX_LEN
from app.models.custombase import CustomBase


class CharityProject(CustomBase):
    """Модель благотворительного проекта."""
    name = Column(String(PR_NAME_MAX_LEN), unique=True, nullable=False)
    description = Column(Text, nullable=False)
