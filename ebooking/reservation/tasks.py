from celery import shared_task, Task
from .mail import send_mail_v2
from .models import *

@shared_task
def async_send_mail(to, reservation_id):
    """ Function that asyncronously send the mail to the client who rent the hotel rooms """
    reservation = Reservation.objects.get(id=reservation_id)
    print("RESERVATION OBEJCT: ",reservation)
    send_mail_v2(to, reservation)