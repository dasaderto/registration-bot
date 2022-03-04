from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from src.framework.localization import L
from src.persistence.user import UserDB
from src.repositories.user_repository import UserRepository
from src.services.base import BaseService


class UserKeyboardService:
    def user_phone_getting_keyboard(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton(text=L("handlers.user_phone_number.buttons.send_phone"), request_contact=True))
        return keyboard

    def user_setup_role_keyboard(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.row(*[
            KeyboardButton(L("handlers.user_role_setup.buttons.master_role")),
            KeyboardButton(L("handlers.user_role_setup.buttons.client_role")),
        ])
        keyboard.add(KeyboardButton(L("handlers.user_role_setup.buttons.all_role")))
        return keyboard


class UserService(BaseService):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.user_repository = UserRepository(db=db)

    async def update(self, user: UserDB, **kwargs):
        for k, v in kwargs.items():
            setattr(user, k, v)
        await self.user_repository.save(model=user)
