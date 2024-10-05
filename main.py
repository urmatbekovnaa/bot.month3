import asyncio
from aiogram import Bot, Dispatcher,  types
from aiogram.filters.command import Command
from dotenv import dotenv_values
import random
import logging

token = dotenv_values('.env')['TOKEN']
bot = Bot(token=token)
dp = Dispatcher()

unique_users = set()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    unique_users.add(message.from_user.id)

    unser_count = len(unique_users)
    await message.answer(f"Здравствуйте , {name}!\n"
                         f"Наш бот обслуживает {unser_count} пользователя(ей). ")

@dp.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    name = message.from_user.first_name
    await message.answer((f'Ваше имя: {name}\n'
                         f'Ваш id: {message.from_user.id}\n'
                         f'Ваш username: {message.from_user.username}'))

@dp.message(Command("random"))
async def random_handler(message: types.Message):
    random_name = random.choice(["Асема", "Ахмад", "Дастан", "Адина", "Ариет", "Эмир"])
    await message.answer(f"Случайное имя: {random_name}")


@dp.message()
async def other_massages_handler(message: types.Message):
    text = message.text
    await message.answer(text)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

