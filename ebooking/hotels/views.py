from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from hotels.models import Hotel, HotelRoom


def index(request):
    all_hotel_objs = Hotel.objects.all()
    context = {"all_hotels": all_hotel_objs}
    return render(request, "home.html", context=context)


def rent_rooms(request, hotel_id):
    hotel_instance = Hotel.objects.get(id=hotel_id)

    if not hotel_instance:
        return HttpResponseForbidden

    hotelRooms = HotelRoom.objects.filter(hotel=hotel_id)
    context ={"hotelrooms": hotelRooms}

    return render(request, template_name='rent_rooms.html', context=context)





