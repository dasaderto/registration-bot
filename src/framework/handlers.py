import functools
from abc import ABC, abstractmethod
from typing import Callable, Optional, Coroutine, Any, Type

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


class BaseStateMachine(ABC):
    def __init__(self, ctx: HandlerContext):
        self.ctx = ctx

    @abstractmethod
    def start(self):
        raise NotImplementedError


def prepare_ctx(state_machine: Type[BaseStateMachine] = None):
    def wrap_handler(wrapped_handler: Callable[[HandlerContext], Coroutine]):
        async def wrapper(message: Message, state: FSMContext):
            async with async_session() as session:
                ctx = HandlerContext(message=message, state=state, db_session=session)
                await wrapped_handler(ctx)
                if state_machine:
                    await state_machine(ctx=ctx).start()

        return wrapper
    return wrap_handler
