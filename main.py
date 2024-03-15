# Завернуть все функции в try  except
# Добавить логирование
# Сохранение в БД
# Оповещение ответственных менеджеров
# Фронтенд

from settings import TOKEN_TG
from tools import calculate_hours, calculate_distance, get_cost, delete_msg, message_dl, log_input, save_order
from message import send_message_hi, edit_message_car_type, edit_message_contact, edit_message_forwarding, \
    edit_message_is_offloading, edit_message_offloading, edit_message_time, edit_message_distance, send_message_cost, \
    edit_message_info, edit_message_hi, send_message_order, last_msg, edit_message_order_successful

import telebot

# Создаем бота
bot = telebot.TeleBot(TOKEN_TG)

# Состояния
states = {}
value_list = {}
# text_msg_info = {}


@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    send_message_hi(bot, message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call.data, states, call.from_user.first_name)

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if chat_id not in states:
        states[chat_id] = ''

    if call.data == "calculate":
        states[chat_id] = 'car_type'
        edit_message_car_type(bot=bot, chat_id=chat_id, message_id=message_id)

    elif call.data == "contacts":
        states[chat_id] = 'contacts'
        edit_message_contact(bot=bot, chat_id=chat_id, message_id=message_id)

    elif call.data in ["car{}".format(i) for i in range(1, 12)]:
        states[chat_id] = 'forwarding'
        edit_message_forwarding(bot=bot, chat_id=chat_id, message_id=message_id)
        if chat_id not in value_list:
            value_list[chat_id] = {}
        value_list[chat_id]['car'] = str(call.data)[3:]

    elif call.data in ["yes", 'no']:
        states[chat_id] = 'is_offloading'
        if call.data == 'yes':
            value_list[chat_id]['forwarding'] = True
        else:
            value_list[chat_id]['forwarding'] = False
        edit_message_is_offloading(bot=bot, chat_id=chat_id, message_id=message_id,
                                   is_forwarding=value_list[chat_id]['forwarding'])

    elif call.data in ["off_yes", "off_no"]:
        states[chat_id] = 'offloading'

        if str(call.data).split('_')[1] == 'yes':
            value_list[chat_id]['is_offloading'] = True
        else:
            value_list[chat_id]['is_offloading'] = False
        edit_message_offloading(bot=bot, chat_id=chat_id, message_id=message_id,
                                is_forwarding=value_list[chat_id]['forwarding'])

    elif call.data.startswith("offloading_") and int(call.data[11:]) in range(1, 11):
        states[chat_id] = 'time'
        off_count = str(call.data).split('_')[1]
        if off_count == '0':
            value_list[chat_id]['is_offloading'] = 0
        value_list[chat_id]['offloading'] = off_count
        edit_message_time(bot=bot, chat_id=chat_id, message_id=message_id)
        last_msg[chat_id] = message_id

    elif call.data in ['time_' + str(i) for i in range(1, 25)]:
        hours = str(call.data).split('_')[1]
        states[chat_id] = 'distance'
        edit_message_distance(bot=bot, chat_id=chat_id, message_id=message_id)
        delete_msg(chat_id)
        value_list[chat_id]['time'] = hours

    elif call.data == "is_right":
        states[chat_id] = 'order'
        cost = get_cost(value_list[chat_id])
        value_list[chat_id]['cost'] = cost
        send_message_cost(bot=bot, chat_id=chat_id, value_list=value_list[chat_id])
        send_message_order(bot=bot, chat_id=chat_id)
        if chat_id in message_dl:
            message_dl[chat_id].append(message_id)
        else:
            message_dl[chat_id] = [message_id]
        delete_msg(chat_id=chat_id)
        log_input(call=call, value_list=value_list[chat_id])

    elif call.data == "back":
        states[chat_id] = 'calculate'
        edit_message_hi(bot=bot, message_id=message_id, chat_id=chat_id)

    elif call.data == "back1":
        states[chat_id] = 'car_type'
        edit_message_car_type(bot=bot, message_id=message_id, chat_id=chat_id)

    elif call.data == "back2":
        states[chat_id] = 'forwarding'
        edit_message_forwarding(bot=bot, message_id=message_id, chat_id=chat_id)

    elif call.data == "back3":
        states[chat_id] = 'is_offloading'
        edit_message_is_offloading(bot=bot, message_id=message_id, chat_id=chat_id,
                                   is_forwarding=value_list[chat_id]['forwarding'])

    elif call.data == "back4":
        states[chat_id] = 'offloading'
        edit_message_offloading(bot=bot, message_id=message_id, chat_id=chat_id,
                                is_forwarding=value_list[chat_id]['forwarding'])

    elif call.data == "back5":
        states[chat_id] = 'time'
        edit_message_time(bot=bot, message_id=message_id, chat_id=chat_id)

    elif call.data == "back6":
        states[chat_id] = 'distance'
        edit_message_distance(bot=bot, message_id=message_id, chat_id=chat_id)

    elif call.data == "main_menu":
        states[chat_id] = 'calculate'
        edit_message_hi(bot=bot, message_id=message_id, chat_id=chat_id)\

    elif call.data == "main_menu_save":
        states[chat_id] = 'calculate'
        edit_message_hi(bot=bot, message_id=message_id, chat_id=chat_id)
        save_order(value_list=value_list[chat_id])


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
            delete_msg(chat_id)
            states[chat_id] = 'distance'
            value_list[chat_id]['time'] = hours
            edit_message_distance(bot=bot, chat_id=chat_id, message_id=last_msg[chat_id])
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
            delete_msg(chat_id)
            states[chat_id] = 'info'
            edit_message_info(bot=bot, chat_id=chat_id, message_id=last_msg[chat_id],
                              value_list=value_list[chat_id])

    elif states[chat_id] == 'order':
        value_list[chat_id]['contact_information'] = message.text
        if chat_id in message_dl:
            message_dl[chat_id].append(message.message_id)
        else:
            message_dl[chat_id] = [message.message_id]
        delete_msg(chat_id)
        states[chat_id] = 'order_successful'
        edit_message_order_successful(bot=bot, chat_id=chat_id, message_id=last_msg[chat_id])
        save_order(value_list=value_list[chat_id])


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
