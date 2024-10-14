from aiogram import Router, F, types
# from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters.command import Command

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Наш сайт",
                    url="https://www.dodopizza.kg/"
                ),
                types.InlineKeyboardButton(
                    text="Наш инстаграм",
                    url="https://www.instagram.com/dodopizza.kg/"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="О нас",
                    callback_data="aboutus"
                ),
                types.InlineKeyboardButton(
                    text="Наши контакты",
                    callback_data="phone"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Вакансии",
                    callback_data="vacancy"
                ),

                types.InlineKeyboardButton(
                    text="Вопросы, Отзывы",
                    url="https://dodopizza.kg/bishkek/contacts"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Адреса пиццерии",
                    callback_data="location"

                )
            ],

        ]
    )
    await message.reply(
        f"Доброго времени суток, {name}. Добро пожаловать в наш бот пиццерии DO DO  ",
        reply_markup=kb)


@start_router.callback_query(F.data == "aboutus")
async def about_us_handler(callback: types.CallbackQuery):
    text = f" DODO вдохновляет нас, заставляет каждое утро просыпаться и с интересом продолжать работу. Чтобы радовать вас нашими вкусными пиццами. "
    await callback.message.answer(text)


@start_router.callback_query(F.data == "phone")
async def phone_handler(callback: types.CallbackQuery):
    text = "Наши контакты:\n 0(312) 550 550\n 0(551) 550 550"
    await callback.message.answer(text)


@start_router.callback_query(F.data == "vacancy")
async def vacancy_handler(callback: types.CallbackQuery):
    text = "Вакансии:\n 1. Кассир\n 2. Курьер\n 3. Оператор:\n" \
           "Отклик на вакансию можно оставить по телефону: 0(312) 550 550"
    await callback.message.answer(text)


@start_router.callback_query(F.data == "location")
async def locations_handler(callback: types.CallbackQuery):
    text = "Адреса пиццерий:\nмкрн. Кок-Жар, 5/1\nпр-т Манаса , 7\nпер. Шевченко, 80"
    await callback.message.answer(text)

