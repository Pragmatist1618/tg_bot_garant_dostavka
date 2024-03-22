from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='short_car_type')
def short_car_type(value):
    car_type_dict = {
        "Газель тент/фургон до 1,5т, 9м³": "Газель",
        "Газель повышенный об. до 1,5т, до 15м³": "Газель",
        "Бычок тент/фургон до 3т, 16м³": "Бычок",
        "5-тонник тент/фургон, 20-36м³": "5-тонник",
        "5-тонник борт, 20-36м³": "5-тонник",
        "10-тонник тент/фургон, 36м³": "10-тонник",
        "10-тонник борт, 36м³": "10-тонник",
        "Ман, Мерседес до 10т, 50м³": "Ман, Мерседес",
        "Еврофура тент до 20т, 82-90м³": "Еврофура",
        "Еврофура борт до 20т, 82-90м³": "Еврофура",
        "Автопоезд до 20т, 100-110м³": "Автопоезд"
    }
    try:
        return car_type_dict[value]
    except Exception as e:
        print(e)
        return value


@register.filter(name='bool_to_text')
def bool_to_text(value):
    if value:
        return 'Да'
    else:
        return 'Нет'


@register.filter(name='contact_info')
def contact_info(value):
    return value[:11]


@register.filter(name='format_price')
def format_price(value):
    try:
        price = int(value)
        formatted_price = '{:,.0f}'.format(price).replace(',', ' ')
        return mark_safe('{} ₽'.format(formatted_price))
    except ValueError:
        return value
