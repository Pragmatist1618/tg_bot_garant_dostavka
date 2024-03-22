from django.contrib import admin
from .models import Order


@admin.register(Order)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'car_type', 'forwarding', 'is_offloading', 'offloading', 'time', 'distance', 'cost', 'contact_information',
        'tg_id', 'tg_username')
    list_filter = (
        'car_type', 'forwarding', 'is_offloading', 'offloading', 'time', 'distance', 'cost', 'contact_information',
        'tg_id', 'tg_username')
    search_fields = (
        'car_type', 'forwarding', 'is_offloading', 'offloading', 'time', 'distance', 'cost', 'contact_information',
        'tg_id', 'tg_username')
