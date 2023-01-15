from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from hotels.models import Hotel, HotelRoom
from .forms import ReservationForm
from django.contrib import messages
from .mail import send_mail, send_mail_v2

def index(request):
    all_hotel_objs = Hotel.objects.all()
    context = {"all_hotels": all_hotel_objs}
    return render(request, "home.html", context=context)

def add_hotel(request):
    # Create form
    # check if post request, check post data
    # if data valid, save object
    return render(request, "add_hotel.html", context={})

def rent_rooms(request, hotel_id):
    hotel_instance = Hotel.objects.get(id=hotel_id)

    if not hotel_instance:
        return HttpResponseForbidden

    form = ReservationForm()
    hotelRooms = HotelRoom.objects.filter(hotel=hotel_id)

    context ={"form":form, "hotelrooms": hotelRooms}
    email_context = {"subject": "Renting confirmation", "rooms":"10"}
    to = "test@ebooking.local" # some name got from front end

    send_mail_v2(email_context, to) 

    if request.method=="POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            send_mail_v2(email_context, to)
        else:
            messages.add_message(request, messages.ERROR, "Date introduse eronat!")
            return render(request, template_name='rent_rooms.html', context=context)
        messages.add_message(request, messages.SUCCESS, "Rezervare facuta cu succes!")
        return redirect('home.html')
    else:
        return render(request, template_name='rent_rooms.html', context=context)





