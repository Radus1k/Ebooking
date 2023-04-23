from django.shortcuts import render, redirect
from reservation.forms import ReservationForm
from django.contrib import messages
from .tasks import async_send_mail
from .models import Reservation
from hotels.models import HotelRoom, Hotel
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from .filters import ReservationFilter
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def reservation_view(request, room_id):
    """
   Function that serves logic of a user reservation form
    """
    form = ReservationForm(is_admin=False)
    # function body here
    if request.method=="POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            user = request.user
            reservation = form.save(commit=False)
            reservation.user = user
            reservation = form.save()
            
            try:
                print("****Sending async email..\n\n\n!")
                async_send_mail.delay(to=user.email, reservation_id=reservation.id)
            except Exception as e:
                print("****\n\n\nCelery worker container/service may be stopped!****\n\n\n!")
            # send_reservation_mail(email_context, to)
            messages.add_message(request, messages.SUCCESS, "Rezervare facuta cu succes! Veti primi detaliile pe email!") 
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, "Oups, a aparut o eroare la incarcare formularului!") 
    else:
        form = ReservationForm()
    context = {"form": form}
    return render(request,"reservation.html",context=context)

@login_required
def reservations_view(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseForbidden()
    if user.is_superuser:
        reservations = Reservation.objects.all()
    elif user.profile.is_hotel_administrator:
        administrator_hotels = user.profile.hotels.all()
        reservations = Reservation.objects.filter(hotelRoom__hotel__in=administrator_hotels)
    elif user.is_authenticated and not user.profile.is_hotel_administrator:
        reservations = Reservation.objects.filter(user=user)

    filter_obj = ReservationFilter(request.GET, queryset=reservations)
    reservations_qs = filter_obj.qs    
    context = {"reservations": reservations_qs, "filter":filter_obj}

    return render(request, 'reservations.html',context=context)

def edit_reservation_view(request, reservation_id):
    user = request.user
    try:
        is_hotel_administrator = user.profile.is_hotel_administrator
    except Exception as e:
        is_hotel_administrator = False 
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST, is_admin=True, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rezervare editata cu succes')
            return redirect('reservation:reservations')
        else:
            messages.success(request, 'A aparut o eroare!')  
            return redirect('reservation:reservations')  
    else:
        form = ReservationForm(instance=reservation, is_admin=is_hotel_administrator)

    context = {'form': form, 'reservation': reservation}
    return render(request, 'edit_reservation.html', context=context)

@login_required
def add_reservation_view(request):
    user = request.user
    try:
        is_hotel_administrator = user.profile.is_hotel_administrator
    except Exception as e:
        is_hotel_administrator = False 
    finally:
        if request.method == 'POST':
            form = ReservationForm(request.POST)
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.save()
                messages.success(request, 'Reservation added successfully.')
                return redirect('reservation:reservations')
            else:
                messages.error(request, 'Reservation data incorrect.')
        else:
            form = ReservationForm(is_admin=is_hotel_administrator)

    context = {'form': form }
    return render(request, 'add_reservation.html', context=context)

@login_required
def delete_reservation_view(request, reservation_id, hotel_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    try:
        reservation.delete()
        messages.success(request, 'Reservation deleted successfully.')
    except:
        messages.error(request, 'Error deleting reservation.')
    return redirect('reservation:reservations')
