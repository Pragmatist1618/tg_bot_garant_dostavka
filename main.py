import os
from django.core.wsgi import get_wsgi_application
from settings import API_TG, managers

# Установка переменной окружения для настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tg_bot_garant_dostavka.settings')

# Загрузка Django приложения
application = get_wsgi_application()

import telebot
from orders.models import Car

# Создаем бота
bot = telebot.TeleBot(API_TG)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Приветствие, краткие пояснения")


# Обработчик выбора типа автомобиля
@bot.message_handler(commands=['order'])
def handle_type(message):
    bot.reply_to(message, "Экспедирование груза (Да/Нет)")


# Обработчик ответа на вопрос об экспедировании груза
@bot.message_handler(func=lambda message: True)
def handle_expedited_cargo(message):
    if message.text.lower() == "да":
        expedited_cargo = True
    else:
        expedited_cargo = False
    bot.reply_to(message, "Выгрузка в ТК с оформлением от 1 до 10 городов (Да/Нет)")
    bot.register_next_step_handler(message, handle_unloading_in_transport_company, expedited_cargo)


# Обработчик ответа на вопрос о выгрузке в ТК
def handle_unloading_in_transport_company(message, expedited_cargo):
    if message.text.lower() == "да":
        unloading_in_transport_company = True
    else:
        unloading_in_transport_company = False
    bot.reply_to(message, "Кол-во мест выгрузки автомобиля (1,2,3,4,5)")
    bot.register_next_step_handler(message, handle_number_of_unloading_places, expedited_cargo,
                                   unloading_in_transport_company)


# Обработчик ответа на вопрос о количестве мест выгрузки
def handle_number_of_unloading_places(message, expedited_cargo, unloading_in_transport_company):
    number_of_unloading_places = int(message.text)
    bot.reply_to(message, "Количество часов работы автомобиля или ориентировочное время работы")
    bot.register_next_step_handler(message, handle_hours_of_work, expedited_cargo, unloading_in_transport_company,
                                   number_of_unloading_places)


# Обработчик ответа на вопрос о количестве часов работы
def handle_hours_of_work(message, expedited_cargo, unloading_in_transport_company, number_of_unloading_places):
    hours_of_work = message.text
    bot.reply_to(message, "Количество пробега за МКАД (км)")
    bot.register_next_step_handler(message, handle_mileage_outside_mkad, expedited_cargo,
                                   unloading_in_transport_company, number_of_unloading_places, hours_of_work)


# Обработчик ответа на вопрос о пробеге за МКАД
def handle_mileage_outside_mkad(message, expedited_cargo, unloading_in_transport_company, number_of_unloading_places,
                                hours_of_work):
    mileage_outside_mkad = int(message.text)
    bot.reply_to(message, "Введите ваши контактные данные")
    bot.register_next_step_handler(message, handle_contact_info, expedited_cargo, unloading_in_transport_company,
                                   number_of_unloading_places, hours_of_work, mileage_outside_mkad)


# Обработчик ввода контактных данных
def handle_contact_info(message, expedited_cargo, unloading_in_transport_company, number_of_unloading_places,
                        hours_of_work, mileage_outside_mkad):
    contact_info = message.text
    # Создаем объект Car и сохраняем его в базе данных
    car = Car.objects.create(
        type=message.text,
        expedited_cargo=expedited_cargo,
        unloading_in_transport_company=unloading_in_transport_company,
        number_of_unloading_places=number_of_unloading_places,
        hours_of_work=hours_of_work,
        mileage_outside_mkad=mileage_outside_mkad,
        contact_info=contact_info
    )

    # Отправляем уведомления менеджерам
    for manager in managers:
        bot.send_message(manager, f"Новый заказ:\n{car}")

    body = '{message}\n' \
           '--\n' \
           '{first}, {last}\n' \
           '{username}, {id}'.format(message=message.text, first=message.from_user.first_name,
                                     last=message.from_user.last_name, username=message.from_user.username,
                                     id=message.chat.id)
    # Открываем файл для записи (если файл не существует, он будет создан)
    with open('orders.log', 'a') as file:
        # Записываем содержимое переменной body в файл
        file.write(body + '\n')

    bot.reply_to(message, "Спасибо! Ваш заказ принят.")


# Запускаем бота
bot.polling()
