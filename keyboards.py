from telebot import types

keyboard_menu = types.InlineKeyboardMarkup()
keyboard_menu.add(types.InlineKeyboardButton("Рассчитать стоимость доставки", callback_data="calculate"),
                  types.InlineKeyboardButton("Контакты", callback_data="contacts"))

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
keyboard_car_type = types.InlineKeyboardMarkup(row_width=1)
keyboard_car_type.add(types.InlineKeyboardButton("Газель тент/фургон до 1,5т, 9м³", callback_data="car1"),
                      types.InlineKeyboardButton("Газель повышенный об. до 1,5т, до 15м³", callback_data="car2"),
                      types.InlineKeyboardButton("Бычок тент/фургон до 3т, 16м³", callback_data="car3"),
                      types.InlineKeyboardButton("5-тонник тент/фургон, 20-36м³", callback_data="car4"),
                      types.InlineKeyboardButton("5-тонник борт, 20-36м³", callback_data="car5"),
                      types.InlineKeyboardButton("10-тонник тент/фургон, 36м³", callback_data="car6"),
                      types.InlineKeyboardButton("10-тонник борт, 36м³", callback_data="car7"),
                      types.InlineKeyboardButton("Ман, Мерседес до 10т, 50м³", callback_data="car8"),
                      types.InlineKeyboardButton("Еврофура тент до 20т, 82-90м³", callback_data="car9"),
                      types.InlineKeyboardButton("Еврофура борт до 20т, 82-90м³", callback_data="car10"),
                      types.InlineKeyboardButton("Автопоезд до 20т, 100-110м³", callback_data="car11"),
                      types.InlineKeyboardButton("Назад", callback_data="back"))

keyboard_ynbe = types.InlineKeyboardMarkup()
keyboard_ynbe.add(types.InlineKeyboardButton("Да", callback_data="yes"),
                  types.InlineKeyboardButton("Нет", callback_data="no"),
                  types.InlineKeyboardButton("Назад", callback_data="back"),
                  types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))

keyboard_off_ynbe = types.InlineKeyboardMarkup()
keyboard_off_ynbe.add(types.InlineKeyboardButton("Да", callback_data="off_yes"),
                      types.InlineKeyboardButton("Нет", callback_data="off_no"),
                      types.InlineKeyboardButton("Назад", callback_data="back"),
                      types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))

keyboard_offloading_5 = types.InlineKeyboardMarkup()
keyboard_offloading_5.add(types.InlineKeyboardButton("1", callback_data="offloading_1"),
                          types.InlineKeyboardButton("2", callback_data="offloading_2"),
                          types.InlineKeyboardButton("3", callback_data="offloading_3"),
                          types.InlineKeyboardButton("4", callback_data="offloading_4"),
                          types.InlineKeyboardButton("5", callback_data="offloading_5"),
                          types.InlineKeyboardButton("Назад", callback_data="back"),
                          types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))

keyboard_offloading_10 = types.InlineKeyboardMarkup()
keyboard_offloading_10.add(types.InlineKeyboardButton("1", callback_data="offloading_1"),
                           types.InlineKeyboardButton("2", callback_data="offloading_2"),
                           types.InlineKeyboardButton("3", callback_data="offloading_3"),
                           types.InlineKeyboardButton("4", callback_data="offloading_4"),
                           types.InlineKeyboardButton("5", callback_data="offloading_5"),
                           types.InlineKeyboardButton("6", callback_data="offloading_6"),
                           types.InlineKeyboardButton("7", callback_data="offloading_7"),
                           types.InlineKeyboardButton("8", callback_data="offloading_8"),
                           types.InlineKeyboardButton("9", callback_data="offloading_9"),
                           types.InlineKeyboardButton("10", callback_data="offloading_10"),
                           types.InlineKeyboardButton("Назад", callback_data="back"),
                           types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))

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

keyboard_time = types.InlineKeyboardMarkup(row_width=4)
hours_buttons = [types.InlineKeyboardButton(str(i), callback_data='time_' + str(i)) for i in range(1, 25)]
keyboard_time.add(*hours_buttons)
keyboard_time.add(types.InlineKeyboardButton("Назад", callback_data="back"),
                  types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))

keyboard_bm = types.InlineKeyboardMarkup()
keyboard_bm.add(types.InlineKeyboardButton("Назад", callback_data="back"),
                types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))

keyboard_info = types.InlineKeyboardMarkup()
# Добавляем кнопку "Все верно" в клавиатуру
keyboard_info.add(types.InlineKeyboardButton("Все верно", callback_data="is_right"))
# Создаем строку для двух остальных кнопок и добавляем их в клавиатуру
row = []
row.append(types.InlineKeyboardButton("Назад", callback_data="back"))
row.append(types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))
keyboard_info.row(*row)

keyboard_back = types.InlineKeyboardMarkup()
keyboard_back.add(types.InlineKeyboardButton("Назад", callback_data="back"))

keyboard_order = types.InlineKeyboardMarkup()
keyboard_order.add(types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))
