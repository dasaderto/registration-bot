from aiogram import types
from src.framework.localization import L
from src.handlers.phone_number_handler import PhoneNumberState


async def start_command(message: types.Message):
    await message.answer(L("commands.start"))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text=L("handlers.user_phone_number.buttons.send_phone"), request_contact=True))
    await PhoneNumberState.phone_number.set()
    await message.answer(L('handlers.user_phone_number.main_message'), reply_markup=keyboard)
