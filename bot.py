from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
import logging
from aiogram import executor


# Токен бота
API_TOKEN = '5431127644:AAE7sIqpkKUYG6q8ErselA3I8Cada2MfasA'
ADMIN_CHAT_ID =  799892391

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Category(StatesGroup):
    establishments = State()
    category = State()
    question = State()
    answer = State()
    new_question = State()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я бот, который поможет тебе найти ответы на вопросы. "
        "Выбери категорию вопросов:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="МВД"),
                    KeyboardButton(text="РОВД"),
                    KeyboardButton(text="ЦОН"),
                    KeyboardButton(text="Паспортный стол"),
                    KeyboardButton(text="Категория 5"),
                ],
            ],
            resize_keyboard=True,
        ),
    )
    await Category.establishments.set()

@dp.message_handler(state=Category.establishments)
async def process_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['establishments'] = message.text

    await message.answer(
        "Выбери вопрос из списка:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
            [
                KeyboardButton(text='МВД'),
                KeyboardButton(text='РОВД'),
                KeyboardButton(text='АРГБ'),
                KeyboardButton(text='УГНС'),
            ],
        ],
        resize_keyboard=True,
        
        ),
    )
    await Category.next()






@dp.message_handler(state=Category.category)
async def process_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await message.answer(
        "Выбери вопрос из списка:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Вопрос 1"),
                    KeyboardButton(text="Вопрос 2"),
                    KeyboardButton(text="Вопрос 3"),
                ],
                [
                    KeyboardButton(text="Свой вопрос"),
                ],

                [
                    KeyboardButton(text="Назад"),
                ],
            ],
            resize_keyboard=True,
        ),
    )
    await Category.next()

@dp.message_handler(
    state=[Category.category, Category.question, Category.answer],
    content_types=types.ContentTypes.TEXT,
    regexp="^Назад$",
)



@dp.message_handler(Text(equals="Свой вопрос"), state=Category.question)
async def process_own_question(message: types.Message):
    await message.answer("Введите свой вопрос:")
    await Category.next()


@dp.message_handler(state=Category.question)
async def process_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text

    await message.answer("Введите свой вопрос:")
    await Category.next()



@dp.message_handler(state=Category.question)
async def process_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text

        # Выполняем логику для обработки вопроса и получения ответа
        answer = 'Ответ на ваш вопрос в разработке. Пожалуйста, попробуйте позже.'

        # Выводим ответ на вопрос
        answer_text = f"Вопрос: {data['question']}\n\nОтвет: {answer}"
        await message.answer(answer_text)

        # Сбрасываем состояние FSM
        await state.finish()


async def process_back_button(message: types.Message, state: FSMContext):
    await message.answer(
        "Выбери категорию вопросов из меню ниже:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Категория 1"),
                    KeyboardButton(text="Категория 2"),
                ],
            ],
            resize_keyboard=True,
        ),
    )
    await Category.set()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)