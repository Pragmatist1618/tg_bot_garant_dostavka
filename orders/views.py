from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order


@login_required
def view_database(request):
    orders = Order.objects.all()
    return render(request, 'view_database.html', {'orders': orders})
