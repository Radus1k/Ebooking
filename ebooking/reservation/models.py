from django.db import models
from hotels.models import *

# Create your models here.

class Reservation(models.Model):
    hotelRoom = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, null=True) # oneToMany
    begin_at = models.CharField(max_length=50)
    ends_at = models.CharField(max_length=50)
    time_in_days = models.PositiveIntegerField(null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    observations = models.CharField(max_length=500)
    phone_no = models.CharField(max_length=15)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

    class Meta:
        db_table = 'reservation'