from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

reviewdialog_router = Router()

class RestourantReview(StatesGroup):
    name = State()
    phone = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


@reviewdialog_router.message(Command("router"))
@reviewdialog_router.callback_query(lambda call: call.data == "feedback")
async def start_feedback_handler(call: types.Message, state: FSMContext):
    await state.set_state(RestourantReview.name)
    await call.message.answer("Добрый день, как вас зовут?")


@reviewdialog_router.message(Command('stop'))
@reviewdialog_router.message(F.text == 'стоп')
async def stop_feedback_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы отменили отзыв.")


@reviewdialog_router.message(RestourantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.set_state(RestourantReview.phone)
    await message.answer("Напишите ваш номер телефона или инстаграм.")


@reviewdialog_router.message(RestourantReview.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.set_state(RestourantReview.visit_date)
    await message.answer("Дата вашего посещения нашего заведения?")


@reviewdialog_router.message(RestourantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.set_state(RestourantReview.food_rating)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="1"),
                types.KeyboardButton(text="2"),
                types.KeyboardButton(text="3"),
                types.KeyboardButton(text="4"),
                types.KeyboardButton(text="5")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Как оцениваете качество еды от 1 до 5?", reply_markup=kb)


@reviewdialog_router.message(RestourantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    await state.set_state(RestourantReview.cleanliness_rating)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="1"),
                types.KeyboardButton(text="2"),
                types.KeyboardButton(text="3"),
                types.KeyboardButton(text="4"),
                types.KeyboardButton(text="5")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Как оцениваете чистоту заведения от 1 до 5?", reply_markup=kb)


@reviewdialog_router.message(RestourantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    await state.set_state(RestourantReview.extra_comments)
    await message.answer("Если ли у вас еще какие-то комментарии?")


@reviewdialog_router.message(RestourantReview.extra_comments)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)

    await message.answer("Спасибо за ваш отзыв!")
    await state.clear()