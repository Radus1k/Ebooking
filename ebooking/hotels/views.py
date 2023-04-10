from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from hotels.models import Hotel, HotelRoom
from django.contrib.auth.decorators import login_required
from .forms import HotelRoomForm, AddHotelRoomForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest
from django.contrib import messages

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
def hotel_rooms_view(request, hotel_id):
    hotel_instance = Hotel.objects.get(id=hotel_id)

    if not hotel_instance:
        return HttpResponseForbidden

    hotelRooms = HotelRoom.objects.filter(hotel=hotel_id)
    context ={"hotelrooms": hotelRooms}

    return render(request, template_name='rent_rooms.html', context=context)


def edit_rooms_view(request, hotel_id):
    hotel_instance = Hotel.objects.get(id=hotel_id)

    if not hotel_instance:
        return HttpResponseForbidden
    
    hotelRooms = HotelRoom.objects.filter(hotel=hotel_id)
    context ={"hotelrooms": hotelRooms, 'hotel_id': hotel_id}


    return render(request, template_name='edit_rooms.html', context=context)


def edit_room_view(request, hotel_id, room_id):
    room = get_object_or_404(HotelRoom, id=room_id, hotel__id=hotel_id)

    if request.method == 'POST':
        form = HotelRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('admin_hotel_rooms', hotel_id=hotel_id)
    else:
        form = HotelRoomForm(instance=room)

    context = {'form': form, 'room': room, }
    return render(request, 'edit_room.html',context=context)


def add_room_view(request, hotel_id):
    if request.method == 'POST':
        form = AddHotelRoomForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            hotelroom = form.save(commit=False)
            hotel = Hotel.objects.get(id=hotel_id)
            hotelroom.hotel = hotel
            hotelroom.save()
            messages.success(request, 'Hotel room added successfully.')
            return redirect('admin_hotel_rooms', hotel_id=hotel_id)
        else:
             messages.error(request, 'Hotel room data incorrect.')
    else:
        form = AddHotelRoomForm(user=request.user)
    return render(request, 'add_room.html', {'form': form})    

def delete_room_view(request, hotel_id, room_id):
    room = get_object_or_404(HotelRoom, id=room_id, hotel__id=hotel_id)
    try:
        room.delete()
        messages.success(request, 'Room deleted successfully.')
    except:
        messages.error(request, 'Error deleting room.')
    return redirect('admin_hotel_rooms', hotel_id=hotel_id)