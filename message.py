from keyboards import *

last_msg = {}

car_type_list = [
    "Газель тент/фургон до 1,5т, 9м³",
    "Газель повышенный об. до 1,5т, до 15м³",
    "Бычок тент/фургон до 3т, 16м³",
    "5-тонник тент/фургон, 20-36м³",
    "5-тонник борт, 20-36м³",
    "10-тонник тент/фургон, 36м³",
    "10-тонник борт, 36м³",
    "Ман, Мерседес до 10т, 50м³",
    "Еврофура тент до 20т, 82-90м³",
    "Еврофура борт до 20т, 82-90м³",
    "Автопоезд до 20т, 100-110м³",
]

offloading_list = [
    'в 1 месте',
    'в 2 местах',
    'в 3 местах',
    'в 4 мастах',
    'в 5 местах',
    'в 6 местах',
    'в 7 местах',
    'в 8 местах',
    'в 9 местах',
    'в 10 местах',
]

text_hi = "Привет! Я бот для оформления заказов на доставку. \nЗдесь Вы можете узнать приблизительную стоимость " \
          "доставки. "
text_car_type = "Выберите тип машины:"
text_contact = "Контактная информация:\nТелефон: +7 495 228-47-97\n                 +7 925 069-60-62\nEmail: " \
               "info@garant-dostavka.ru\nСайт:https://garant-dostavka.ru/",
text_forwarding = "Экспедирование груза машины:"
text_is_offloading_fy = "Выгрузка в ТК с оформлением от 1 до 10 городов:"
text_is_offloading_fn = "Выгрузка в ТК с оформлением от 1 до 5 городов:"
text_offloading = "Укажите количество мест выгрузки:"
text_time = "Количество часов работы автомобиля (можно указать диапазон в формате '10.00-15.45'):"
text_distance = "Введите числом количество пробега за МКАД (км):"
text_msg_info = ("*Вы указали следующие данные:*\n\n"
                 "_Тип машины:_ *%s*\n\n"
                 "_Экспедирование груза машины:_ *%s*\n\n"
                 "_Выгрузка в ТК:_ *%s*\n\n"
                 "_Количество мест выгрузки:_ *%s*\n\n"
                 "_Количество часов работы автомобиля:_ *%s*\n\n"
                 "_Количество пробега за МКАД (км):_ *%s*\n\n")
text_order = "Укажите контактную информацию для обратной связи (отправьте в чат):"
text_order_successful = "Ваш заказ передан менеджеру. В ближайшее время с Вами свяжутся."


def send_message(bot, chat_id, text, keyboard):
    a = bot.send_message(chat_id=chat_id, text=text,
                         reply_markup=keyboard, parse_mode="Markdown")
    last_msg[chat_id] = a.message_id
    print(last_msg)


def send_message_hi(bot, chat_id):
    send_message(bot, chat_id, text_hi, keyboard_menu)


def edit_message(bot, chat_id, message_id, text, keyboard):
    bot.edit_message_text(text=text, message_id=message_id, chat_id=chat_id, parse_mode="Markdown")
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)


def edit_message_car_type(bot, chat_id, message_id):
    edit_message(bot=bot, text=text_car_type, message_id=message_id, chat_id=chat_id, keyboard=keyboard_car_type)


def edit_message_contact(bot, chat_id, message_id):
    edit_message(bot=bot, text=text_contact, message_id=message_id, chat_id=chat_id, keyboard=keyboard_back)


def edit_message_forwarding(bot, chat_id, message_id):
    edit_message(bot=bot, text=text_forwarding, message_id=message_id, chat_id=chat_id, keyboard=keyboard_ynbe)


def edit_message_is_offloading(bot, chat_id, message_id, is_forwarding):
    if is_forwarding:
        edit_message(bot=bot, text=text_is_offloading_fy, message_id=message_id, chat_id=chat_id,
                     keyboard=keyboard_off_ynbe)
    else:
        edit_message(bot=bot, text=text_is_offloading_fn, message_id=message_id, chat_id=chat_id,
                     keyboard=keyboard_off_ynbe)


def edit_message_offloading(bot, chat_id, message_id, is_forwarding):
    if is_forwarding:
        edit_message(bot=bot, text=text_offloading, message_id=message_id, chat_id=chat_id,
                     keyboard=keyboard_offloading_10)
    else:
        edit_message(bot=bot, text=text_offloading, message_id=message_id, chat_id=chat_id,
                     keyboard=keyboard_offloading_5)


def edit_message_time(bot, chat_id, message_id):
    edit_message(bot=bot, text=text_time, message_id=message_id, chat_id=chat_id, keyboard=keyboard_time)


def edit_message_distance(bot, chat_id, message_id):
    edit_message(bot=bot, text=text_distance, message_id=message_id, chat_id=chat_id, keyboard=keyboard_bm)


def get_info(value_list):
    car_type = value_list['car']
    if value_list['forwarding']:
        forwarding = 'да'
    else:
        forwarding = 'нет'
    if value_list['is_offloading']:
        is_offloading = 'да'
    else:
        is_offloading = 'нет'
    offloading = offloading_list[int(value_list['offloading']) - 1]
    time = value_list['time']
    distance = value_list['distance']
    return text_msg_info % (
        car_type_list[int(car_type) - 1], forwarding, is_offloading, offloading, time, distance)


def send_message_cost(bot, chat_id, value_list):
    message = get_info(value_list) + '\n' + 'Расчетная стоимость: ' + str(value_list['cost'])
    send_message(bot, chat_id, message, None)


def send_message_order(bot, chat_id):
    send_message(bot, chat_id, text_order, keyboard_order)
    return


def edit_message_info(bot, chat_id, message_id, value_list):
    edit_message(bot=bot, text=get_info(value_list), message_id=message_id, chat_id=chat_id, keyboard=keyboard_info)


def edit_message_hi(bot, chat_id, message_id):
    edit_message(bot=bot, text=text_hi, message_id=message_id, chat_id=chat_id, keyboard=keyboard_menu)


def edit_message_order_successful(bot, chat_id, message_id):
    edit_message(bot=bot, text=text_order_successful, message_id=message_id, chat_id=chat_id, keyboard=keyboard_menu)
