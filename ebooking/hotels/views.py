from django.shortcuts import render
from django.http import HttpResponse
from hotels.models import Hotel

def index(request):
    all_hotel_objs = Hotel.objects.all()
    context = {"all_hotels": all_hotel_objs}
    return render(request, "home.html", context=context)

def add_hotel(request):
    # Create form
    # check if post request, check post data
    # if data valid, save object
    return render(request, "add_hotel.html", context={})
