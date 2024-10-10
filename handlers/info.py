from aiogram import Router, types
from aiogram.filters.command import Command
info_router = Router()

@info_router.message(Command("myinfo"))
async def info_handler(message: types.Message):
    name = message.from_user.first_name
    await message.answer((f'Ваше имя: {name}\n'
                         f'Ваш id: {message.from_user.id}\n'
                         f'Ваш username: {message.from_user.username}'))
