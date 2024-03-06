from django.shortcuts import render
from .models import Car


def view_database(request):
    cars = Car.objects.all()
    return render(request, 'view_database.html', {'cars': cars})
