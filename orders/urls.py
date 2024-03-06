from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_database, name='orders'),  # URL-шаблон для просмотра базы данных
]
