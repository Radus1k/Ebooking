from django.shortcuts import render, redirect
from reservation.forms import ReservationForm
from django.contrib import messages
from .tasks import async_send_mail
from .models import Reservation
from hotels.models import HotelRoom

# Create your views here.

def reservation_view(request, room_id):
    if request.method=="POST":
        messages.add_message(request, messages.SUCCESS, "Rezervare facuta cu succes!")
        # form = ReservationForm(request.POST)
        hotelRoom = HotelRoom.objects.get(id=room_id)
        first_name = request.POST['data_2']
        last_name = request.POST['data_3']
        phone_number = request.POST['data_4']
        email = request.POST['data_5']
        check_in = request.POST['data_6']
        check_out = request.POST['data_7']
        observations = request.POST['data_10']

        reservation = Reservation(hotelRoom = hotelRoom, begin_at=check_in, ends_at=check_out, observations=observations,phone_number=phone_number, first_name=first_name, last_name=last_name)
        reservation.save()

        async_send_mail.delay(to=email, reservation_id=reservation.id)
        #send_mail_v2(email_context, to)
        return redirect('home')
    else:
        return render(request,"reservation.html",{})