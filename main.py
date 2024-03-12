# Завернуть все функции в try  except

import os

import requests
from django.core.wsgi import get_wsgi_application

from keyboards import *
from settings import API_TG
from tools import calculate_hours, calculate_distance, get_cost

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
last_msg = {}


@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот для оформления заказов на доставку. \n "
                                      "Здесь Вы можете узнать приблизительную стоимость доставки.",
                     reply_markup=keyboard_menu)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # print(call.data, states)
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
        bot.edit_message_text(text="Экспедирование груза машины:",
                              message_id=message_id, chat_id=chat_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_ynbe)
    # Выгрузка в ТК с оформлением от 1 до 10 городов
    elif call.data in ["yes", 'no']:
        states[chat_id] = 'is_offloading'
        value_list[chat_id]['forwarding'] = call.data
        if call.data == 'yes':
            bot.edit_message_text(text="Выгрузка в ТК с оформлением от 1 до 10 городов:",
                                  message_id=message_id, chat_id=chat_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_off_ynbe)
            is_ex[chat_id] = True  # <============
        else:
            bot.edit_message_text(text="Выгрузка в ТК с оформлением от 1 до 5 городов:",
                                  message_id=message_id, chat_id=chat_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_off_ynbe)

    elif call.data in ["off_yes", "off_no"]:
        states[chat_id] = 'offloading'
        value_list[chat_id]['is_offloading'] = str(call.data).split('_')[1]
        if value_list[chat_id]['forwarding'] == 'yes':
            bot.edit_message_text(text="Укажите количество мест выгрузки:",
                                  message_id=message_id, chat_id=chat_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_offloading_10)
        else:
            bot.edit_message_text(text="Укажите количество мест выгрузки:",
                                  message_id=message_id, chat_id=chat_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_offloading_5)

    elif call.data in ["offloading_1", "offloading_2", "offloading_3", "offloading_4", "offloading_5", "offloading_6",
                       "offloading_7", "offloading_8", "offloading_9", "offloading_10"]:
        states[chat_id] = 'time'
        off_count = str(call.data).split('_')[1]
        # print('offcount', off_count)
        if off_count == '0':
            value_list[chat_id]['is_offloading'] = 0
        value_list[chat_id]['offloading'] = off_count
        bot.edit_message_text(
            text="Количество часов работы автомобиля (можно указать диапазон в формате '10.00-15.45'):",
            message_id=message_id, chat_id=chat_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_time)
        last_msg[chat_id] = message_id

    elif call.data in ['time_' + str(i) for i in range(1, 25)]:
        hours = str(call.data).split('_')[1]
        states[chat_id] = 'distance'
        if chat_id in message_dl:
            for messaged_id in message_dl[chat_id]:
                url = f'https://api.telegram.org/bot{API_TG}/deleteMessage?chat_id={chat_id}&message_id={messaged_id}'
                requests.get(url)
        value_list[chat_id]['time'] = hours
        bot.edit_message_text(
            text="Введите числом количество пробега за МКАД (км):",
            message_id=message_id, chat_id=chat_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_bm)
    if call.data == "is_right":
        states[chat_id] = 'order'
        # ID чата
        chat_id = call.message.chat.id
        # Имя пользователя
        user_name = call.from_user.first_name
        # ID пользователя
        user_id = call.from_user.id
        print("User Name:", user_name)
        print("User ID:", user_id)
        print(value_list)
        cost = get_cost(value_list[chat_id])
        bot.edit_message_text(
            text='Расчетная стоимость: ' + str(cost),
            message_id=message_id, chat_id=chat_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_order)

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
        elif states[chat_id] == "is_offloading":
            states[chat_id] = 'forwarding'
            bot.edit_message_text("Экспедирование груза машины:", chat_id, message_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_ynbe)
        elif states[chat_id] == "offloading":
            states[chat_id] = 'is_offloading'
            if value_list[chat_id]['forwarding'] == 'yes':
                bot.edit_message_text("Выгрузка в ТК с оформлением от 1 до 10 городов:", chat_id, message_id)
                bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                              reply_markup=keyboard_off_ynbe)
            else:
                bot.edit_message_text("Выгрузка в ТК с оформлением от 1 до 5 городов:", chat_id, message_id)
                bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                              reply_markup=keyboard_off_ynbe)
        elif states[chat_id] == "time":
            states[chat_id] = 'offloading'
            bot.edit_message_text("Укажите количество мест выгрузки:", chat_id, message_id)
            if is_ex[chat_id]:
                bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                              reply_markup=keyboard_offloading_10)
            else:
                bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                              reply_markup=keyboard_offloading_5)
        elif states[chat_id] == "distance":
            states[chat_id] = 'time'
            bot.edit_message_text(
                text="Количество часов работы автомобиля (можно указать диапазон в формате '10.00-15.45'):",
                message_id=message_id, chat_id=chat_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_time)
            last_msg[chat_id] = message_id
        elif states[chat_id] == "info":
            states[chat_id] = 'distance'
            bot.edit_message_text(
                text="Введите числом количество пробега за МКАД (км):",
                message_id=message_id, chat_id=chat_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_bm)

    elif call.data == "main_menu":
        states[chat_id] = 'calculate'
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
            if chat_id in message_dl:
                for message_id in message_dl[chat_id]:
                    url = f'https://api.telegram.org/bot{API_TG}/deleteMessage?chat_id={chat_id}&message_id={message_id}'
                    requests.get(url)
                    states[chat_id] = 'distance'
                    value_list[chat_id]['time'] = hours
                bot.edit_message_text(
                    text="Введите число - количество пробега за МКАД (км):",
                    message_id=last_msg[chat_id], chat_id=chat_id)
                bot.edit_message_reply_markup(chat_id=chat_id, message_id=last_msg[chat_id],
                                              reply_markup=keyboard_bm)
    elif states[chat_id] == 'distance':
        distance = calculate_distance(message.text)
        if chat_id in message_dl:
            message_dl[chat_id].append(message.message_id)
        else:
            message_dl[chat_id] = [message.message_id]
        if distance is None:
            sent_message = bot.send_message(chat_id, "Некорректный запрос, повторите снова: ")
            message_dl[chat_id].append(sent_message.message_id)
        else:
            value_list[chat_id]['distance'] = distance
            if chat_id in message_dl:
                for message_id in message_dl[chat_id]:
                    url = f'https://api.telegram.org/bot{API_TG}/deleteMessage?chat_id={chat_id}&message_id={message_id}'
                    requests.get(url)
                states[chat_id] = 'info'
                car_type = value_list[chat_id]['car']
                if value_list[chat_id]['forwarding'] == 'no':
                    forwarding = 'нет'
                else:
                    forwarding = 'да'
                if value_list[chat_id]['is_offloading'] == 'no':
                    is_offloading = 'нет'
                else:
                    is_offloading = offloading_list[int(value_list[chat_id]['offloading'])]
                time = value_list[chat_id]['time']
                distance = value_list[chat_id]['distance']
                text_msg = f"*Вы указали следующие данные:*\n\n" \
                           f"_Тип машины:_ *{car_type_list[int(car_type) - 1]}*\n\n" \
                           f"_Экспедирование груза машины:_ *{forwarding}*\n\n" \
                           f"_Выгрузка в ТК:_ *{is_offloading}*\n\n" \
                           f"_Количество часов работы автомобиля:_ *{time}*\n\n"  \
                           f"_Количество пробега за МКАД (км):_ *{distance}*\n\n"
                bot.edit_message_text(
                    text=text_msg,
                    message_id=last_msg[chat_id], chat_id=chat_id, parse_mode="Markdown")
                bot.edit_message_reply_markup(chat_id=chat_id, message_id=last_msg[chat_id],
                                              reply_markup=keyboard_info)


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
