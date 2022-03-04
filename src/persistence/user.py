from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSON

from src.framework.localization import L
from src.persistence.base import BaseDBModel, ChoicesEnum


class UserRoles(ChoicesEnum):
    MASTER = L("handlers.user_role_setup.buttons.master_role")
    CLIENT = L("handlers.user_role_setup.buttons.client_role")


class UserDB(BaseDBModel):
    __tablename__ = "users"

    tg_first_name = Column(String(255))
    tg_last_name = Column(String(255), nullable=True)
    tg_username = Column(String(255), nullable=True)
    tg_raw_user = Column(JSON)

    phone = Column(String(255), nullable=True)
    role = Column(String(50), nullable=True)
