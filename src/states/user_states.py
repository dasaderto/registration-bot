from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    phone_number = State()
    user_role = State()
