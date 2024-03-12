import math
from datetime import datetime


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
