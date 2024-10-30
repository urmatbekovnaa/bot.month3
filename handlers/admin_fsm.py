import sqlite3

from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import database


class FoodAdd(StatesGroup):
    name = State()
    category = State()
    price = State()
    weight = State()
    confirm = State()


class CategoryAdd(StatesGroup):
    name = State()


admin_add_router = Router()
admin = 1014937406
admin_add_router.message.filter(F.from_user.id == admin)


@admin_add_router.message(Command("add_category"))
async def start_category_add(message: types.Message, state: FSMContext):
    await state.set_state(CategoryAdd.name)
    await message.answer("Введите название категории:")


@admin_add_router.message(CategoryAdd.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    database.execute(
        query="INSERT INTO categories (category_name) VALUES (?)",
        params=(name,)
    )
    await state.clear()
    await message.answer("Категория успешно добавлена!")


@admin_add_router.message(Command("add_food"))
async def start_food_add(message: types.Message, state: FSMContext):
    await state.set_state(FoodAdd.name)
    await message.answer("Введите название блюда:")


@admin_add_router.message(FoodAdd.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.title())
    await state.set_state(FoodAdd.category)

    categories = database.fetch(
        query="SELECT name FROM categories")

    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=category[0])] for category in categories],
        resize_keyboard=True)

    await message.answer("Выберите подходящую категорию блюда:", reply_markup = kb)
    await state.set_state(FoodAdd.category)


@admin_add_router.message(FoodAdd.category)
async def process_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Введите цену блюда:")
    await state.set_state(FoodAdd.price)


@admin_add_router.message(FoodAdd.price)
async def process_price(m: types.Message, state: FSMContext):

    if m.text.isdigit():
        await state.update_data(price=m.text)
        await m.answer("Введите вес блюда:")
        await state.set_state(FoodAdd.weight)
    else:
        await m.answer("Пожалуйста, введите корректное число!!")


@admin_add_router.message(FoodAdd.weight)
async def process_weight(m: types.Message, state: FSMContext):
    if m.text.isdigit():
        await state.update_data(weight=m.text)
        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="confirm"),
                    types.KeyboardButton(text="cancel")
                ]
            ],
            resize_keyboard=True
        )
        await state.set_state(FoodAdd.confirm)
    else:
        await m.answer("Пожалуйста, введите корректное число!!")


@admin_add_router.message(FoodAdd.confirm)
async def process_confirm(m: types.Message, state: FSMContext, db=database):
    if m.text == 'confirm':
        data = await state.get_data()
        category_id = database.fetch(
            query="SELECT id FROM categories WHERE category_name = ?",
            params=(data['category'],)
        )[0][0]

        database.execute('''
            INSERT INTO dishes(name,category, price, weight, category_id) VALUES (?, ?, ?, ?, ?)
            ''',
                         (data['name'], data['category'], data['price'], data['weight'], category_id)
                         )
        await state.clear()
    elif m.text == 'cancel':
        await m.answer("Отмена добавления блюда")
        await state.clear()
    else:
        await m.answer("Confirm or Cancel.")
