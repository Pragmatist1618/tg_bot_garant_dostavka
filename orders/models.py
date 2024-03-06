from django.db import models


class Car(models.Model):
    type = models.CharField(max_length=100, verbose_name='Тип автомобиля')
    expedited_cargo = models.BooleanField(verbose_name='Экспедирование груза')
    unloading_in_transport_company = models.BooleanField(verbose_name='Выгрузка в ТК с оформлением')
    number_of_unloading_places = models.IntegerField(verbose_name='Количество мест выгрузки')
    hours_of_work = models.CharField(max_length=100, verbose_name='Часы работы')
    mileage_outside_mkad = models.IntegerField(verbose_name='Пробег за МКАД')
    contact_info = models.CharField(max_length=100, verbose_name='Контактная информация')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'