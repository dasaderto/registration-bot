from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSON

from src.persistence.base import BaseDBModel


class UserDB(BaseDBModel):
    __tablename__ = "users"

    tg_first_name = Column(String(255))
    tg_last_name = Column(String(255), nullable=True)
    tg_username = Column(String(255), nullable=True)
    tg_raw_user = Column(JSON)

    phone = Column(String(255), nullable=True)
