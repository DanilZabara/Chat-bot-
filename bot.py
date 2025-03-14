import os 
import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем кнопки
btn_phone = KeyboardButton(text="📞 Надати номер", request_contact=True)
btn_fop = KeyboardButton(text="ФОП")
btn_tov = KeyboardButton(text="ТОВ")
btn_raben = KeyboardButton(text="Рабен")
btn_nova_poshta = KeyboardButton(text="Нова Пошта")
btn_new_order = KeyboardButton(text="🆕 Оформити нове замовлення")

# Глобальная переменная для хранения данных
user_data = {}

# Функция для генерации номера заказа
def generate_order_number():
    return datetime.now().strftime("%Y%m%d%H%M%S")

# Начальное меню
@dp.message(lambda message: message.text == "/start" or message.text == "🆕 Оформити нове замовлення")
async def start(message: types.Message):
    user_data[message.from_user.id] = {}  # Очищаем предыдущие данные
    markup = ReplyKeyboardMarkup(keyboard=[[btn_phone]], resize_keyboard=True)
    await message.answer("Вітаю! Надайте ваш номер телефону 📞", reply_markup=markup)

# Получаем номер телефона
@dp.message(lambda message: message.contact is not None)
async def get_phone(message: types.Message):
    user_data[message.from_user.id]['phone'] = message.contact.phone_number
    markup = ReplyKeyboardMarkup(keyboard=[[btn_fop, btn_tov]], resize_keyboard=True)
    await message.answer("Оберіть тип оплати:", reply_markup=markup)

# Выбор ФОП/ТОВ
@dp.message(lambda message: message.text in ["ФОП", "ТОВ"])
async def get_payment_type(message: types.Message):
    user_data[message.from_user.id]['payment'] = message.text
    await message.answer("Напишіть, на кого виставити рахунок (назва компанії або ПІБ)")

# Получаем название компании
@dp.message(lambda message: message.text and message.from_user.id in user_data and 'payment' in user_data[message.from_user.id])
async def get_company_name(message: types.Message):
    user_data[message.from_user.id]['company'] = message.text
    await message.answer("Яку каву бажаєте замовити? Пропишіть назву та кількість зерна в кг. (приклад: 'Бразилія Черадо - 2 кг')")

# Получаем заказ
@dp.message(lambda message: "-" in message.text)
async def get_order(message: types.Message):
    user_data[message.from_user.id]['order'] = message.text
    markup = ReplyKeyboardMarkup(keyboard=[[btn_raben, btn_nova_poshta]], resize_keyboard=True)
    await message.answer("Оберіть службу доставки:", reply_markup=markup)

# Выбор доставки
@dp.message(lambda message: message.text in ["Рабен", "Нова Пошта"])
async def get_delivery(message: types.Message):
    user_data[message.from_user.id]['delivery'] = message.text
    await message.answer("Пропишіть адресу доставки (місто, вулиця, номер дому, або відділення Нової Пошти)")

# Получение адреса и отправка админу
@dp.message()
async def get_address(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {}  # Создаем запись для нового пользователя
    
    user_data[user_id]['address'] = message.text
    order_number = generate_order_number()
    user_data[user_id]['order_number'] = order_number  # Сохраняем номер заказа

    # Формируем текст заказа
    order_text = (
        f"📌 Нове замовлення #{order_number}\n"
        f"📞 Телефон: {user_data[user_id].get('phone', 'Не указан')}\n"
        f"💳 Оплата: {user_data[user_id].get('payment', 'Не указана')}\n"
        f"🏢 Компанія: {user_data[user_id].get('company', 'Не вказана')}\n"
        f"☕ 
