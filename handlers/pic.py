from aiogram import Router, types
from aiogram.filters import Command


random_router = Router()


@random_router.message(Command("pic"))
async def picture_handler(message: types.Message):
    image = types.FSInputFile("images/мясная.jpg")
    await message.answer_photo(
        photo=image,
        caption="Рецепт мясной пиццы:\n цыпленок , ветчина из цыпленка , пепперони из цыпленка , колбаски чоризо из цыпленка , моцарелла, томатный соус"
    )

