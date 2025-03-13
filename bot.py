import os
import logging
import asyncio
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
btn_phone = KeyboardButton(text="📞 Отправить номер", request_contact=True)
btn_fop = KeyboardButton(text="ФОП")
btn_tov = KeyboardButton(text="ТОВ")
btn_raben = KeyboardButton(text="Рабен")
btn_nova_poshta = KeyboardButton(text="Новая Почта")

# Глобальная переменная для хранения данных
user_data = {}

# Начальное меню
@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    user_data[message.from_user.id] = {}
    markup = ReplyKeyboardMarkup(keyboard=[[btn_phone]], resize_keyboard=True)
    await message.answer("Привет! Отправь мне свой номер телефона 📞", reply_markup=markup)

# Получаем номер телефона
@dp.message(lambda message: message.contact is not None)
async def get_phone(message: types.Message):
    user_data[message.from_user.id]['phone'] = message.contact.phone_number
    markup = ReplyKeyboardMarkup(keyboard=[[btn_fop, btn_tov]], resize_keyboard=True)
    await message.answer("Выбери тип оплаты:", reply_markup=markup)

# Выбор ФОП/ТОВ
@dp.message(lambda message: message.text in ["ФОП", "ТОВ"])
async def get_payment_type(message: types.Message):
    user_data[message.from_user.id]['payment'] = message.text
    await message.answer("Напиши название зерна и количество (пример: 'Арабика - 2 кг')")

# Получаем заказ
@dp.message(lambda message: "-" in message.text)
async def get_order(message: types.Message):
    user_data[message.from_user.id]['order'] = message.text
    markup = ReplyKeyboardMarkup(keyboard=[[btn_raben, btn_nova_poshta]], resize_keyboard=True)
    await message.answer("Выбери службу доставки:", reply_markup=markup)

# Выбор доставки
@dp.message(lambda message: message.text in ["Рабен", "Новая Почта"])
async def get_delivery(message: types.Message):
    user_data[message.from_user.id]['delivery'] = message.text
    await message.answer("Отправь адрес доставки (город, улица, номер дома)")

# Получение адреса и отправка админу
@dp.message()
async def get_address(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['address'] = message.text

    # Формируем текст заказа
    order_text = (
        f"📌 Новый заказ!\n"
        f"📞 Телефон: {user_data[user_id]['phone']}\n"
        f"💳 Оплата: {user_data[user_id]['payment']}\n"
        f"☕ Заказ: {user_data[user_id]['order']}\n"
        f"🚚 Доставка: {user_data[user_id]['delivery']}\n"
        f"🏠 Адрес: {user_data[user_id]['address']}"
    )

    # Отправляем админу
    await bot.send_message(chat_id=ADMIN_ID, text=order_text)
    await message.answer("✅ Заказ принят! Мы скоро свяжемся с вами.")

# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
