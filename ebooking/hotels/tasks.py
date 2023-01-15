from celery import shared_task, Task
from .mail import send_mail_v2
from .models import *

@shared_task
def async_send_mail(to, hotel_id):
    """ Function that asyncronously send the mail to the client who rent the hotel rooms """
    hotelRooms = HotelRoom.objects.filter(hotel=hotel_id).first()
    send_mail_v2(to, hotelRooms)