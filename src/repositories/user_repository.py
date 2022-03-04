import logging

from aiogram.types import User

from src.persistence.user import UserDB
from src.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository):
    async def get_or_create_from_tg(self, tg_user: User) -> UserDB:
        query = await self.exec_query(self.select(UserDB).where(UserDB.id == tg_user.id))
        user = query.scalars().first()
        if not user:
            user = UserDB()
            user.id = tg_user.id
        user.tg_first_name = tg_user.first_name
        user.tg_last_name = tg_user.last_name
        user.tg_username = tg_user.username
        user.tg_raw_user = tg_user.to_python()
        self.db.add(user)
        await self.db.commit()
        return user
