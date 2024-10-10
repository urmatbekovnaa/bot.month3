from aiogram import Router, types
from aiogram.filters.command import Command
import random

random_router = Router()


@random_router.message(Command("random"))
async def send_picture(message: types.Message):
    image = types.FSInputFile("images/pizza.jpg")
    await message.answer_photo(
        photo=image,
        caption="Цыпленок, моцарелла, сладкий перец , красный лук , острый перец халапеньо , "
                "томаты , соус сальса, томатный соус"
    )

