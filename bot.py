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
async def get_payment_type(message: types.Message):
    user_data[message.from_user.id]['payment'] = message.text
    await message.answer("Напиши название зерна и количество (пример: 'Арабика - 2 кг')")

@dp.message(lambda message: "-" in message.text)
async def get_order(message: types.Message):
    user_data[message.from_user.id]['order'] = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_raben, btn_nova_poshta)
    await message.answer("Выбери службу доставки:", reply_markup=markup)

@dp.message(lambda message: message.text in ["Рабен", "Новая Почта"])
async def get_delivery(message: types.Message):
    user_data[message.from_user.id]['delivery'] = message.text
    await message.answer("Отправь адрес доставки (город, улица, номер дома)")

@dp.message()
async def get_address(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['address'] = message.text

    order_text = (
        f"📌 Новый заказ!\n"
        f"📞 Телефон: {user_data[user_id]['phone']}\n"
        f"💳 Оплата: {user_data[user_id]['payment']}\n"
        f"☕ Заказ: {user_data[user_id]['order']}\n"
        f"🚚 Доставка: {user_data[user_id]['delivery']}\n"
        f"🏠 Адрес: {user_data[user_id]['address']}"
    )

    await bot.send_message(ADMIN_ID, order_text)
    await message.answer("✅ Заказ принят! Мы скоро свяжемся с вами.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем вебхук
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
