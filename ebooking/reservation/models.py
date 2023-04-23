from django.db import models
from hotels.models import *
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

choices = ('In asteptare','Confirmata','Anulata')
class Reservation(models.Model):
    IN_ASTEPTARE = 'In asteptare'
    CONFIRMATA = 'Confirmata'
    ANULATA = 'Anulata'
    STATUS_CHOICES = [
        (IN_ASTEPTARE, 'In asteptare'),
        (CONFIRMATA, 'Confirmata'),
        (ANULATA, 'Anulata'),
    ]
    hotelRoom = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, null=True) # oneToMany
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False) # oneToMany
    begin_at = models.DateTimeField(blank=False, default=datetime.datetime.now, null=False)
    ends_at = models.DateTimeField(blank=False, default=datetime.datetime.now, null=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    observations = models.CharField(max_length=500,blank=True, null=True)
    phone_no = models.CharField(max_length=15)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default=IN_ASTEPTARE)

    class Meta:
        db_table = 'reservation'
    
    def duration_in_days(self):
        delta = self.ends_at - self.begin_at
        return delta.days

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " reservation at " + self.hotelRoom.hotel.name + " at " + self.hotelRoom.__str__()
