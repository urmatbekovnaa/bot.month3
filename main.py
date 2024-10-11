import asyncio
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
import logging

#
from handlers.start import start_router
from handlers.info import info_router
from handlers.random import random_router
from handlers.other_messange import other_router

token = dotenv_values('.env')['TOKEN']
bot = Bot(token=token)
dp = Dispatcher()


async def main():
    dp.include_router(start_router)
    dp.include_router(info_router)
    dp.include_router(random_router)

    dp.include_router(other_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
