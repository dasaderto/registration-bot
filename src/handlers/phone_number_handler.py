from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from src.framework.localization import L


class PhoneNumberState(StatesGroup):
    phone_number = State()


async def user_phone_number_handler(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    await state.finish()
    await message.answer(L('handlers.user_phone_number.success'))

