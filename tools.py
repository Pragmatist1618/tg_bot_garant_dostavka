import math
import os
from datetime import datetime

import requests

from django.core.wsgi import get_wsgi_application

from settings import TOKEN_TG

# Установка переменной окружения для настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tg_bot_garant_dostavka.settings')
# Загрузка Django приложения
application = get_wsgi_application()
from orders.models import Car

message_dl = {}


def calculate_hours(time_str):
    try:
        # Удаляем все символы, кроме цифр, чтобы оставить только числа
        time_str = ''.join(filter(str.isdigit, time_str))
        # Преобразуем строку времени в формат времени (часы и минуты)
        start_time = datetime.strptime(time_str[:4], '%H%M')
        end_time = datetime.strptime(time_str[4:], '%H%M')
        # Вычисляем разницу между начальным и конечным временем
        time_difference = end_time - start_time
        # Переводим разницу времени в часы и округляем вверх
        total_hours = time_difference.seconds / 3600
        total_hours = math.ceil(total_hours)
        return total_hours
    except ValueError:
        # print("Некорректный формат времени. Пожалуйста, введите время в формате HHMM.")
        return None


def calculate_distance(distance_str):
    try:
        distance = float(distance_str)
        return math.ceil(distance)
    except ValueError:
        return None


def get_cost(value_list):
    price_t = [900, 930, 1100, 1350, 1550, 1450, 1950, 2100, 2400, 2550, 2750]
    min_h = [5, 5, 6, 8, 8, 8, 8, 8, 8, 8, 8]
    price_d = [35, 40, 44, 50, 55, 60, 60, 70, 90, 90, 95]

    car_type = int(value_list['car']) - 1
    if value_list['forwarding'] == 'no':
        forwarding = 0
    else:
        forwarding = 1
    if value_list['is_offloading'] == 'no':
        is_offloading = 0
    else:
        is_offloading = 1
    offloading = int(value_list['offloading']) - 1
    if offloading < 0:
        offloading = 0

    time = int(value_list['time'])
    if time < min_h[car_type]:
        time = min_h[car_type]

    distance = int(value_list['distance'])

    total_h = time + 1 + forwarding + offloading + is_offloading

    coast = total_h * price_t[car_type] + distance * price_d[car_type]

    log_dict = {
        'car_type': car_type,
        'forwarding': forwarding,
        'is_offloading': is_offloading,
        'offloading': offloading,
        'time': time,
        'distance': distance,
        'total_h': total_h,
        'coast': coast,
    }

    print(log_dict)

    return coast


def delete_msg(chat_id):
    if chat_id in message_dl:
        for messaged_id in message_dl[chat_id]:
            url = f'https://api.telegram.org/bot{TOKEN_TG}/deleteMessage?chat_id={chat_id}&message_id={messaged_id}'
            requests.get(url)
        message_dl[chat_id] = []


def log_input(call, value_list):
    # ID чата
    chat_id = call.message.chat.id
    # Имя пользователя
    user_name = call.from_user.first_name
    # ID пользователя
    user_id = call.from_user.id
    print("User Name:", user_name)
    print("User ID:", user_id)
    print(value_list)


def save_order(value_list):
    pass