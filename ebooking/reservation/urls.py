from django.urls import path
from .views import *


app_name = 'reservation'

urlpatterns = [
    path('', hotel_reservations, name='hotel_reservations'),
    path('<int:room_id>/', reservation_view, name='reservation'),  # User registering reservation

    # Admin related endpoints
    path('hotel_reservations/', hotel_reservations, name='hotel_reservations'),
    path('edit/<int:reservation_id>/', edit_reservation_view, name='edit_reservation'), # 
    path('add/', add_reservation_view, name='add_reservation'), # 
    path('delete/<int:reservation_id><int:hotel_id>/', delete_reservation_view, name='delete_reservation'), # User rUser reserva# User reservation
]
