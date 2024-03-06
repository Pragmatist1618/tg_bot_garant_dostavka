import os

from django.core.wsgi import get_wsgi_application

from keyboards import *
from settings import API_TG

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


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот для оформления заказов на доставку. \n "
                                      "Здесь Вы можете узнать приблизительную стоимость доставки.",
                     reply_markup=keyboard_menu)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
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
        bot.edit_message_text(text="Экспедирование груза машина:",
                              message_id=message_id, chat_id=chat_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_ynbe)
    elif call.data in ["yes", 'no']:
        states[chat_id] = 'offloading'
        if call.data == 'yes':
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
        off_count = str(call.data)[-1] if str(call.data)[-1] != '0' else 10
        print(off_count)
        bot.edit_message_text(text="Экспедирование груза машина:",
                              message_id=message_id, chat_id=chat_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_ynbe)
    elif call.data == "back":
        if states[chat_id] == "contacts" or states[chat_id] == "car_type":
            bot.edit_message_text("Привет! Я бот для оформления заказов на доставку. \n "
                                  "Здесь Вы можете узнать приблизительную стоимость доставки.", chat_id, message_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_menu)
        elif states[chat_id] == "forwarding":
            bot.edit_message_text("Выберите тип машины:", chat_id, message_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_car_type)
        elif states[chat_id] == "Offloading":
            bot.edit_message_text("Экспедирование груза машина:", chat_id, message_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboard_ynbe)
    elif call.data == "main_menu":
        bot.edit_message_text("Привет! Я бот для оформления заказов на доставку. \n "
                              "Здесь Вы можете узнать приблизительную стоимость доставки.", chat_id, message_id)
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                      reply_markup=keyboard_menu)

        # # Создание инлайн-клавиатуры
        # def create_inline_keyboard():
        #     keyboard = types.InlineKeyboardMarkup(row_width=3)
        #     for i in range(0, 10, 3):
        #         buttons = [types.InlineKeyboardButton(str(j), callback_data=str(j)) for j in range(i, i + 3)]
        #         keyboard.add(*buttons)
        #     keyboard.add(types.InlineKeyboardButton("Подтвердить", callback_data="confirm"),
        #                  types.InlineKeyboardButton("Стереть", callback_data="clear"))
        #     return keyboard
        #
        # # Обработчик команды /start
        # @bot.message_handler(commands=['start'])
        # def handle_start(message):
        #     bot.send_message(message.chat.id, "Введите число от 0 до 9999:", reply_markup=create_inline_keyboard())
        #
        # # Обработчик нажатий на кнопки
        # @bot.callback_query_handler(func=lambda call: True)
        # def handle_callback_query(call):
        #     if call.data.isdigit():
        #         bot.answer_callback_query(call.id, f"Вы выбрали число {call.data}")
        #     elif call.data == "confirm":
        #         bot.answer_callback_query(call.id, "Подтверждено")
        #     elif call.data == "clear":
        #         bot.answer_callback_query(call.id, "Стерто")


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
