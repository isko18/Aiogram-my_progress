from aiogram import Bot,types, Dispatcher, executor
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import os
import time


load_dotenv(".env")

from start import CustomDB

db = CustomDB()
connect = db.connect
db.connect_db()


inline_buttons = [
    InlineKeyboardButton('Старт', callback_data='start'),
    InlineKeyboardButton('Помощь', callback_data='help'),
    InlineKeyboardButton('Backend', callback_data='Backend'),
    InlineKeyboardButton('Frontend', callback_data='Frontend'),
    InlineKeyboardButton('Uxui', callback_data='Uxui'),
    InlineKeyboardButton('Android', callback_data='Android'),
    InlineKeyboardButton('IOS', callback_data='ios'),
  


]

button = InlineKeyboardMarkup().add(*inline_buttons)

bot = Bot(os.environ.get('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    cursor = connect.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"INSERT INTO users VALUES ('{message.from_user.username}', '{message.from_user.first_name}', '{message.from_user.last_name}', {message.from_user.id}, '{time.ctime()}');")
    await message.answer(f'Здравствуйте {message.from_user.full_name}')
    await message.answer("Приветсвую вас в IT академии, My_progress")
    await message.answer("Здесь вы можете выбрать себе направление\nЧтобы узнать подробнее выберите один из этих направлениий👇")
    await message.answer("Если запутаетесь в командах напишите /help", reply_markup=button)
    connect.commit()

@dp.callback_query_handler(lambda call: call)
async def all(call):
    if call.data == "start":
        await start(call.message)
    elif call.data == "help":
        await helper(call.message)
    elif call.data == "Backend":
        await back(call.message)
    elif call.data == "Frontend":
        await front(call.message)
    elif call.data == "Uxui":
        await ux(call.message)
    elif call.data == "Android":
        await andr(call.message)
    elif call.data == "ios":
        await ios(call.message)
   


@dp.message_handler(commands=['help'])
async def helper(message:types.Message):
    await message.answer("Для связи с админом обращайтесь: isko")


@dp.message_handler(commands=['Backend'])
async def back(message:types.Message):
    await message.answer("Backend — это внутренняя часть сайта и сервера и т.д\nСтоимость 10000 сом в месяц\nОбучение: 5 месяц")


@dp.message_handler(commands=['Frontend'])
async def front(message:types.Message):
    await message.answer("Frontend — Frontend — это разработка пользовательского интерфейса и функций, которые работают на клиентской стороне веб-сайта или приложения.\nСтоимость 10000 сом в месяц\nОбучение: 5 месяц")


@dp.message_handler(commands=['Uxui'])
async def ux(message:types.Message):
    await message.answer("Uxui — это внутренняя часть сайта и сервера и т.д\nСтоимость 10000 сом в месяц\nОбучение: 3 месяц")


@dp.message_handler(commands=['Android'])
async def andr(message:types.Message):
    await message.answer("Android — Создаёт приложения и поддерживает их работу\nСтоимость 10000 сом в месяц\nОбучение: 7 месяц")

@dp.message_handler(commands=['ios'])
async def ios(message:types.Message):
    await message.answer("IOS — это создание максимально привлекательного, интуитивно понятного и отзывчивого интерфейса.\nСтоимость 10000 сом в месяц\nОбучение: 7 месяц")


executor.start_polling(dp)