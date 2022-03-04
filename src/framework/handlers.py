import functools
from typing import Callable, Optional, Coroutine, Any

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database import async_session
from src.persistence.user import UserDB
from src.repositories.user_repository import UserRepository


class HandlerContext:
    _user: UserDB = None

    def __init__(self, message: Message, state: FSMContext, db_session: AsyncSession):
        self.message = message
        self.state = state
        self.db = db_session

    @property
    async def user(self) -> UserDB:
        if not self._user:
            async with async_session() as session:
                repository = UserRepository(db=session)
                self._user = await repository.get_or_create_from_tg(tg_user=self.message.from_user)
        return self._user


def prepare_ctx(wrapped_handler: Callable[[HandlerContext], Coroutine]):
    async def wrapper(message: Message, state: FSMContext):
        async with async_session() as session:
            ctx = HandlerContext(message=message, state=state, db_session=session)
            await wrapped_handler(ctx)
    return wrapper
