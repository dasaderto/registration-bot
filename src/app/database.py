from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from src.cfg.current_config import Config

DB_DSN = f"postgresql+asyncpg://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}"

engine = create_async_engine(DB_DSN, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()

