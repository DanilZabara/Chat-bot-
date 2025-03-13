import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # Приводим к int (на случай, если .env отсутствует)

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Создаем кнопки
btn_phone = KeyboardButton("📞 Отправить номер", request_contact=True)
btn_fop = KeyboardButton("ФОП")
btn_tov = KeyboardButton("ТОВ")
btn_raben = KeyboardButton("Рабен")
btn_nova_poshta = KeyboardButton("Новая Почта")

# Глобальная переменная для хранения данных
user_data = {}

# Начальное меню
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_data[message.from_user.id] = {}
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_phone)
    await message.answer("Привет! Отправь мне свой номер телефона 📞", reply_markup=markup)

# Получаем номер телефона
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_phone(message: types.Message):
    user_data[message.from_user.id]['phone'] = message.contact.phone_number
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_fop, btn_tov)
    await message.answer("Выбери тип оплаты:", reply_markup=markup)

# Выбор ФОП/ТОВ
@dp.message_handler(lambda message: message.text in ["ФОП", "ТОВ"])
async def get_payment_type(message: types.Message):
    user_data[message.from_user.id]['payment'] = message.text
    await message.answer("Напиши название зерна и количество (пример: 'Арабика - 2 кг')")

# Получаем заказ
@dp.message_handler(lambda message: "-" in message.text)
a
