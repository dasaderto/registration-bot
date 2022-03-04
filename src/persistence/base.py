from enum import Enum

import sqlalchemy
from sqlalchemy import Column, Integer

from src.app.database import Base


class ChoicesEnum(str, Enum):
    @classmethod
    def has(cls, value: str):
        return value in cls._value2member_map_


class BaseDBModel(Base):
    __abstract__ = True

    id: Column = sqlalchemy.Column(Integer, primary_key=True, index=True)