from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import database

admin_add_router = Router()

class FoodAdd(StatesGroup):
    name = State()
    category = State()
    price = State()
    weight = State()
    confirm = State()


admin = 1014937406

@admin_add_router.message(Command("add_food"))
async def start_food_add(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        await message.answer("Введите название блюда:")
        await state.set_state(FoodAdd.name)
    else:
        await message.answer("Вы не админ!!!")

@admin_add_router.message(FoodAdd.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.title())
    await message.answer("Введите категорию блюда:")
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
        await m.answer('Введите confirm для добавление, \n или cancel для отмены.')
        await state.set_state(FoodAdd.confirm)
    else:
        await m.answer("Пожалуйста, введите корректное число!!")

@admin_add_router.message(FoodAdd.confirm)
async def process_confirm(m: types.Message, state: FSMContext, db=database):
    if m.text == 'confirm':
        await m.answer("Блюдо добавлено.")
        data = await state.get_data()
        database.execute('''
            INSERT INTO foods(name,category, price, weight) VALUES (?, ?, ?, ?)
            ''',
                         (data['name'], data['category'], data['price'], m.text)
                         )
        await state.clear()
    elif m.text == 'cancel':
        await m.answer("Отмена добавления блюда.")
        await state.clear()
    else:
        await m.answer("confirm or cancel.")
