from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
    'type', 'expedited_cargo', 'unloading_in_transport_company', 'number_of_unloading_places', 'hours_of_work',
    'mileage_outside_mkad', 'contact_info')
    list_filter = ('type', 'expedited_cargo', 'unloading_in_transport_company', 'number_of_unloading_places')
    search_fields = ('type', 'contact_info')
