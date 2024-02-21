from django.urls import path
from .views import delivery_fee

urlpatterns = [
    path('calculate/', delivery_fee, name='calculate_fee'),
]