from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from hotels.models import Hotel, HotelRoom
from django.contrib.auth.decorators import login_required
from .forms import HotelRoomForm
from django.urls import reverse_lazy

def index(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse_lazy('accounts:log_in'))
    user = request.user

    if not user.is_authenticated:   
        all_hotel_objs = Hotel.objects.all()
    else:
        if user.profile.is_hotel_administrator:
            all_hotel_objs = user.profile.hotels.all()
        else:
            all_hotel_objs = Hotel.objects.all()
    
    context = {"all_hotels": all_hotel_objs}
    return render(request, "home.html", context=context)

@login_required
def rent_rooms(request, hotel_id):
    hotel_instance = Hotel.objects.get(id=hotel_id)

    if not hotel_instance:
        return HttpResponseForbidden

    hotelRooms = HotelRoom.objects.filter(hotel=hotel_id)
    context ={"hotelrooms": hotelRooms}

    return render(request, template_name='rent_rooms.html', context=context)


def edit_rooms(request, hotel_id):
    hotel_instance = Hotel.objects.get(id=hotel_id)

    if not hotel_instance:
        return HttpResponseForbidden
    form = HotelRoomForm()
    if request.method == "POST":
        completed_form = HotelRoomForm(request.POST)

        if completed_form.is_valid():
            completed_form.save()        
    hotelRooms = HotelRoom.objects.filter(hotel=hotel_id)        
    context ={"form": form, "hotelrooms":hotelRooms}

    return render(request, template_name='edit_rooms.html', context=context)


