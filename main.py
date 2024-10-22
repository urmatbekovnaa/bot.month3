import asyncio
import logging
from aiogram import Bot

from config import bot, dp, database
from handlers.start import start_router
from handlers.info import info_router
from handlers.pic import random_router
from handlers.review_diolog import reviewdialog_router
from handlers.admin_fsm import admin_add_router
from handlers.other_messange import other_router


async def on_startup(bot: Bot):
    database.create_table()


async def main():
    dp.include_router(start_router)
    dp.include_router(info_router)
    dp.include_router(random_router)
    dp.include_router(reviewdialog_router)
    dp.include_router(admin_add_router)
    dp.include_router(other_router)

    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

