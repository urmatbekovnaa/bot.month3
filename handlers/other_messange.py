from aiogram import Router, types
from aiogram.filters.command import Command

other_router = Router()


@other_router.message()
async def other_massages_handler(message: types.Message):
    # text = message.text
    await message.answer("sorry, i don't understand you")