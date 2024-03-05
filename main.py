import telebot
import sqlite3

# Установка токена вашего бота
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)

# Создание или подключение к базе данных SQLite
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# Создание таблицы для хранения заказов, если она ещё не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_type TEXT,
                expedited_cargo TEXT,
                unload_in_tc TEXT,
                unload_places INTEGER,
                work_hours TEXT,
                mileage_km INTEGER,
                contact_info TEXT)''')
conn.commit()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для оформления заказов на доставку товаров. "
                          "Для начала работы нажмите /order.")

# Обработчик команды /order
@bot.message_handler(commands=['order'])
def start_order(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Давайте начнем оформление заказа.\n"
                              "Выберите тип автомобиля (Грузовик, Фургон, Пикап):")
    bot.register_next_step_handler(message, get_car_type)

# Функция для получения типа автомобиля
def get_car_type(message):
    chat_id = message.chat.id
    car_type = message.text

    bot.send_message(chat_id, "Спасибо! Вы выбрали {}.".format(car_type))
    bot.send_message(chat_id, "Вопрос1: Экспедирование груза (Да/Нет):")
    bot.register_next_step_handler(message, get_expedited_cargo, car_type)

# Функция для получения информации об экспедировании груза
def get_expedited_cargo(message, car_type):
    chat_id = message.chat.id
    expedited_cargo = message.text.lower()

    bot.send_message(chat_id, "Вопрос2: Выгрузка в ТК с оформлением от 1 до 10 городов (Да/Нет):")
    bot.register_next_step_handler(message, get_unload_in_tc, car_type, expedited_cargo)