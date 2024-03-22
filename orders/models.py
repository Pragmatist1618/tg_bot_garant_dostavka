from django.db import models


class Order(models.Model):
    car_type = models.CharField(max_length=100, verbose_name='Тип автомобиля')
    forwarding = models.BooleanField(verbose_name='Экспедирование груза')
    is_offloading = models.BooleanField(verbose_name='Выгрузка в ТК с оформлением')
    offloading = models.IntegerField(verbose_name='Количество мест выгрузки')
    time = models.CharField(max_length=100, verbose_name='Часы работы')
    distance = models.IntegerField(verbose_name='Пробег за МКАД')
    cost = models.IntegerField(verbose_name='Итоговая стоимость')
    contact_information = models.CharField(max_length=100, verbose_name='Контактная информация')
    tg_id = models.CharField(max_length=100, verbose_name='ID Telegram пользователя')
    tg_username = models.CharField(max_length=100, verbose_name='Имя пользователя в Telegram')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'