from aiogram import F, Router, types
from aiogram.filters import Command

from config import database

dishes_router = Router()


@dishes_router.message(Command("catalog"))
async def catalog_handler(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Горячии блюда"),
                types.KeyboardButton(text="Салаты")
            ],
            [
                types.KeyboardButton(text="Десерты"),
                types.KeyboardButton(text="Напитки"),
                types.KeyboardButton(text="Закуски")

            ]
        ],
        resize_keyboard = True,
        input_field_placeholder = "Выберите категорию"
    )
    await message.answer("Выберите категорию:", reply_markup=kb)

categories = ("Горячие блюда", "Салаты", "Десерты", "Напитки", "Закуски")


@dishes_router.message(F.text.in_(categories))
async def show_dishes_by_category(message: types.Message):
    category = message.text
    print(f"{category}")
    dishes = database.fetch(
        query="SELECT * FROM dishes WHERE category = ?",
        params=(category,))
    print(dishes)
    if len(dishes) == 0:
        await message.answer(f"В категории '{category}' пока нет блюд.")

    await message.answer(f"В категории '{category}' есть следующие блюда:")
    for dish in dishes:
        msg = f"Название: {dish['name']} \nC ценой: {dish['price']} сом\nИ весом: {dish['weight']} грамм"
        await message.answer(msg)
