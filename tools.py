import math
from datetime import datetime


def calculate_hours(time_str):
    while True:
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