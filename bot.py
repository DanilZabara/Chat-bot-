import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # Приводим к int

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кнопки
btn_phone = KeyboardButton("📞 Отправить номер", request_contact=True)
btn_fop = KeyboardButton("ФОП")
btn_tov = KeyboardButton("ТОВ")
btn_raben = KeyboardButton("Рабен")
btn_nova_poshta = KeyboardButton("Новая Почта")

# Глобальная переменная для хранения данных
user_data = {}

@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    user_data[message.from_user.id] = {}
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_phone)
    await message.answer("Привет! Отправь мне свой номер телефона 📞", reply_markup=markup)

@dp.message(lambda message: message.contact)
async def get_phone(message: types.Message):
    user_data[message.from_user.id]['phone'] = message.contact.phone_number
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_fop, btn_tov)
    await message.answer("Выбери тип оплаты:", reply_markup=markup)

@dp.message(lambda message: message.text in ["ФОП", "ТОВ"])
async def get_payment_type(messa
