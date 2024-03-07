import os

import requests
from django.core.wsgi import get_wsgi_application

from keyboards import *
from settings import API_TG
from tools import calculate_hours

# Установка переменной окружения для настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tg_bot_garant_dostavka.settings')
# Загрузка Django приложения
application = get_wsgi_application()
import telebot

# from orders.models import Car


# Создаем бота
bot = telebot.TeleBot(API_TG)

# Состояния
states = {}
value_list = {}
message_dl = {}
is_ex = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот для оформления заказов на доставку. \n "
                                      "Здесь Вы можете узнать приблизительную стоимость доставки.",
                     reply_markup=keyboard_menu)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call.data, states)
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if chat_id not in states:
        states[chat_id] = ''
    # посчитать
    if call.data == "calculate":
        states[chat_id] = 'car_type'
        bot.edit_message_text(text="Выберите тип машины:", message_id=message_id, chat_id=chat_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard_car_type)
    # контакты
    elif call.data == "contacts":
        states[chat_id] = 'contacts'
        bot.edit_message_text(text="Контактная информация:\nТелефон: +123456789\nEmail: example@example.com",
                              message_id=message_id, chat_id=chat_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_back)
    # тип машины
    elif call.data in ["car1", "car2", "car3", "car4", "car5", "car6", "car7", "car8", "car9", "car10", "car11"]:
        states[chat_id] = 'forwarding'
        if chat_id not in value_list:
            value_list[chat_id] = {}
        value_list[chat_id]['car'] = str(call.data)[3:]
        bot.edit_message_text(text="Экспедирование груза машина:",
                              message_id=message_id, chat_id=chat_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_ynbe)
    # Выгрузка в ТК с оформлением от 1 до 10 городов


    elif call.data in ["yes", 'no']:
        states[chat_id] = 'offloading'
        value_list[chat_id]['forwarding'] = call.data
        if call.data == 'yes':
            bot.edit_message_text(text="Укажите количество мест выгрузки:",
                                  message_id=message_id, chat_id=chat_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_offloading_10)
            is_ex[chat_id] = True #<============
        else:
            bot.edit_message_text(text="Укажите количество мест выгрузки:",
                                  message_id=message_id, chat_id=chat_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_offloading_5)
    elif call.data in ["offloading_1", "offloading_2", "offloading_3", "offloading_4", "offloading_5", "offloading_6",
                       "offloading_7", "offloading_8", "offloading_9", "offloading_10"]:
        states[chat_id] = 'time'
        off_count = str(call.data)[-1] if str(call.data)[-1] != '0' else 10
        value_list[chat_id]['offloading'] = off_count
        bot.edit_message_text(
            text="Количество часов работы автомобиля (можно указать диапазон в формате '10.00-15.45'):",
            message_id=message_id, chat_id=chat_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_time)

    elif call.data in ['time_' + str(i) for i in range(1, 25)]:
        hours = str(call.data).split('_')[1]
        states[chat_id] = 'distance'
        if chat_id in message_dl:
            for message_id in message_dl[chat_id]:
                url = f'https://api.telegram.org/bot{API_TG}/deleteMessage?chat_id={chat_id}&message_id={message_id}'
                requests.get(url)
        value_list[chat_id]['time'] = hours
        print(value_list)

    # -количество пробега за МКАД (км)


    elif call.data == "back":
        if states[chat_id] == "contacts" or states[chat_id] == "car_type":
            states[chat_id] = 'calculate'
            bot.edit_message_text("Привет! Я бот для оформления заказов на доставку. \n "
                                  "Здесь Вы можете узнать приблизительную стоимость доставки.", chat_id, message_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_menu)
        elif states[chat_id] == "forwarding":
            states[chat_id] = 'car_type'
            bot.edit_message_text("Выберите тип машины:", chat_id, message_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_car_type)
        elif states[chat_id] == "offloading":
            states[chat_id] = 'forwarding'
            bot.edit_message_text("Экспедирование груза машина:", chat_id, message_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_ynbe)
        elif states[chat_id] == "time":
            states[chat_id] = 'offloading'
            bot.edit_message_text("Укажите количество мест выгрузки:", chat_id, message_id)
            if chat_id in is_ex:
                if is_ex[chat_id]:
                    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_offloading_10)
                else:
                    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                  reply_markup=keyboard_offloading_5)
    elif call.data == "main_menu":
        bot.edit_message_text("Привет! Я бот для оформления заказов на доставку. \n "
                              "Здесь Вы можете узнать приблизительную стоимость доставки.", chat_id, message_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_menu)


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    if chat_id not in states:
        states[chat_id] = ''
    if states[chat_id] == 'time':
        hours = calculate_hours(message.text)
        if chat_id in message_dl:
            message_dl[chat_id].append(message.message_id)
        else:
            message_dl[chat_id] = [message.message_id]
        if hours is None:
            sent_message = bot.send_message(chat_id, "Некорректный запрос, повторите снова: ")
            message_dl[chat_id].append(sent_message.message_id)
        else:
            # if chat_id in message_dl:
            #     for message_id in message_dl[chat_id]:
            #         url = f'https://api.telegram.org/bot{API_TG}/deleteMessage?chat_id={chat_id}&message_id={message_id}'
            #         requests.get(url)
            callback_data = "time_" + str(hours)  # Здесь формируется callback_data
            callback_inline(callback_data)


# # Обработчик ввода контактных данных
# def handle_contact_info(message, expedited_cargo, unloading_in_transport_company, number_of_unloading_places,
#                         hours_of_work, mileage_outside_mkad):
#     contact_info = message.text
#     # Создаем объект Car и сохраняем его в базе данных
#     car = Car.objects.create(
#         type=message.text,
#         expedited_cargo=expedited_cargo,
#         unloading_in_transport_company=unloading_in_transport_company,
#         number_of_unloading_places=number_of_unloading_places,
#         hours_of_work=hours_of_work,
#         mileage_outside_mkad=mileage_outside_mkad,
#         contact_info=contact_info
#     )
#
#     # Отправляем уведомления менеджерам
#     for manager in managers:
#         bot.send_message(manager, f"Новый заказ:\n{car}")
#
#     body = '{message}\n' \
#            '--\n' \
#            '{first}, {last}\n' \
#            '{username}, {id}'.format(message=message.text, first=message.from_user.first_name,
#                                      last=message.from_user.last_name, username=message.from_user.username,
#                                      id=message.chat.id)
#     # Открываем файл для записи (если файл не существует, он будет создан)
#     with open('orders.log', 'a') as file:
#         # Записываем содержимое переменной body в файл
#         file.write(body + '\n')
#
#     bot.reply_to(message, "Спасибо! Ваш заказ принят.")
# # Запускаем бота
bot.polling()
