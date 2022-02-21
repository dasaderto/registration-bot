import sqlalchemy
from sqlalchemy import Column, Integer

from src.app.database import Base


class BaseDBModel(Base):
    __abstract__ = True

    id: Column = sqlalchemy.Column(Integer, primary_key=True, index=True)