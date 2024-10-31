from aiogram import F, Router, types
from aiogram.filters import Command
from config import database
from itertools import islice

dishes_router = Router()


def batched(iterable, n):
    it = iter(iterable)
    while True:
        batch = tuple(islice(it, n))
        if not batch:
            break
        yield batch


@dishes_router.message(Command("catalog"))
async def catalog_handler(message: types.Message):
    categories = database.fetch("SELECT category_name FROM categories")
    COLUMNS = 3
    categories_by_three = list(batched(categories, COLUMNS))


    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Выберите категорию")]
        ],
        resize_keyboard=True
    )
    for row in categories_by_three:
        kb.row(*[types.KeyboardButton(text=cat['name']) for cat in row])

    await message.answer("Выберите категорию:", reply_markup=kb)


def categories_filter(message: types.Message):
    category = message.text.lower()
    categories = database.fetch(
        query="SELECT * FROM categories WHERE LOWER(category_name) = ?",
        params=(category,)
    )

    if categories:
        return {'category': categories[0]['category_name']}
    else:
        return False


@dishes_router.message(categories_filter)
async def show_dishes_by_category(message: types.Message, category: str):
    dishes = database.fetch(
        query="""
            SELECT * FROM dishes
            JOIN categories ON dishes.category = categories.id
            WHERE LOWER(categories.name) = ?""",
        params=(category.lower(),)
    )

    if not dishes:
        await message.answer(f"В категории '{category}' пока нет блюд.")
    else:
        await message.answer(f"В категории '{category}' есть следующие блюда:")
        for dish in dishes:
            msg = f"Название: {dish['name']} \nЦена: {dish['price']} сом\nВес: {dish['weight']} грамм"
            await message.answer(msg)
