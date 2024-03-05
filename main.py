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


# Функция для получения информации о выгрузке в транспортной компании
def get_unload_in_tc(message, car_type, expedited_cargo):
    chat_id = message.chat.id
    unload_in_tc = message.text.lower()

    if unload_in_tc == 'да':
        bot.send_message(chat_id, "Спасибо! Укажите количество городов для оформления:")
        bot.register_next_step_handler(message, get_unload_places, car_type, expedited_cargo, unload_in_tc)
    else:
        bot.send_message(chat_id, "Вопрос3: Кол-во мест выгрузки автомобиля (1,2,3,4,5):")
        bot.register_next_step_handler(message, get_unload_places, car_type, expedited_cargo, unload_in_tc)


# Функция для получения количества мест выгрузки автомобиля
def get_unload_places(message, car_type, expedited_cargo, unload_in_tc):
    chat_id = message.chat.id
    unload_places = message.text

    bot.send_message(chat_id, "Спасибо! Теперь укажите количество часов работы автомобиля или "
                              "ориентировочное время работы (например, с 9:00 до 12:00):")
    bot.register_next_step_handler(message, get_work_hours, car_type, expedited_cargo, unload_in_tc, unload_places)


# Функция для получения информации о времени работы автомобиля
def get_work_hours(message, car_type, expedited_cargo, unload_in_tc, unload_places):
    chat_id = message.chat.id
    work_hours = message.text

    bot.send_message(chat_id, "Укажите количество пробега за МКАД (км):")
    bot.register_next_step_handler(message, get_mileage_km, car_type, expedited_cargo, unload_in_tc,
                                   unload_places, work_hours)


# Функция для получения информации о пробеге за МКАД
def get_mileage_km(message, car_type, expedited_cargo, unload_in_tc, unload_places, work_hours):
    chat_id = message.chat.id
    mileage_km = message.text

    bot.send_message(chat_id, "Введите свои контактные данные:")
    bot.register_next_step_handler(message, get_contact_info, car_type, expedited_cargo, unload_in_tc,
                                   unload_places, work_hours, mileage_km)


# Функция для получения контактной информации и завершения заказа
def get_contact_info(message, car_type, expedited_cargo, unload_in_tc, unload_places, work_hours, mileage_km):
    chat_id = message.chat.id
    contact_info = message.text

    # Записываем данные заказа в базу данных
    cursor.execute('''INSERT INTO orders (car_type, expedited_cargo, unload_in_tc, unload_places,
                      work_hours, mileage_km, contact_info) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (car_type, expedited_cargo, unload_in_tc,
                                                        unload_places, work_hours, mileage_km, contact_info))
    conn.commit()

    # Отправляем уведомление менеджерам о новом заказе
    send_notification_to_managers()

    bot.send_message(chat_id, "Ваш заказ принят. Мы свяжемся с вами в ближайшее время.")


# Функция для отправки уведомления менеджерам о новом заказе
def send_notification_to_managers():
    # Здесь можно добавить логику отправки уведомления менеджерам
    pass


# Запуск бота
bot.polling()
