from aiogram import types
from aiogram.dispatcher import FSMContext

from framework.localization import L


async def start_command(message: types.Message, state: FSMContext):
    await message.answer(L("commands.start"))
